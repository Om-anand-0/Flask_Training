from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Room, Participant, User
from app import db, socketio
from flask_socketio import emit, join_room, leave_room, rooms

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/dashboard')
@login_required
def dashboard():
    rooms = [p.room for p in current_user.rooms_joined]
    all_rooms = Room.query.all()
    return render_template('chat/dashboard.html', rooms=rooms, all_rooms=all_rooms)


@chat_bp.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        description = request.form.get('description')
        room = Room(name=room_name, description=description, created_by=current_user.id)
        db.session.add(room)
        db.session.commit()
        participants = Participant(room_id=room.id, user_id=current_user.id)
        db.session.add(participants)
        db.session.commit()
        return redirect(url_for('chat.dashboard'))
    return render_template('chat/create_room.html')


@chat_bp.route('/join_room/<int:room_id>', methods=['POST'])
@login_required
def join_room_http(room_id):
    check = Participant.query.filter_by(room_id=room_id, user_id=current_user.id).first()
    if not check:
        participant = Participant(room_id=room_id, user_id=current_user.id)
        db.session.add(participant)
        db.session.commit()
    return redirect(url_for('chat.dashboard'))


@chat_bp.route('/room/<int:room_id>')
@login_required
def chat_room(room_id):
    from app.models import Room
    room = Room.query.get_or_404(room_id)
    return render_template('chat/chat_room.html', room=room)

@chat_bp.route('/leave_room/<int:room_id>', methods=['POST'])
@login_required
def leave_room_http(room_id):
    participant = Participant.query.filter_by(room_id=room_id, user_id=current_user.id).first()
    if participant:
        db.session.delete(participant)
        db.session.commit()
        socketio.emit('message', {'msg': f'{current_user.username} left the room permanently', 'username': 'System'}, room=str(room_id))
    return redirect(url_for('chat.dashboard'))



@socketio.on('connect')
def handle_connect():
    print(f"DEBUG: Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"DEBUG: Client disconnected: {request.sid}")

@socketio.on('join_room')
def handle_join(data):
    from app.models import Room
    
    print(f"DEBUG: join_room event received: {data}")
    room_id = str(data['room_id'])
    join_room(room_id)
    
    room = Room.query.get(int(room_id))
    room_name = room.name if room else room_id
    
    print(f"DEBUG: User {current_user.username} (sid={request.sid}) joined room {room_name} ({room_id})")
    print(f"DEBUG: Current rooms for socket {request.sid}: {rooms()}")

    emit('message', {'msg': f'{current_user.username} has joined the room', 'username': 'System'}, room=room_id)

@socketio.on('send_message')
def handle_send_message(data):
    from app.models import Message
    
    print(f"DEBUG: send_message event received: {data}")
    room_id = str(data['room_id'])
    content = data['message']
    

    new_message = Message(
        room_id=room_id,
        user_id=current_user.id,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()
    print(f"DEBUG: Message saved to DB with ID: {new_message.id}")

    
    print(f"DEBUG: Broadcasting message '{content}' from {current_user.username} to room {room_id}")
    print(f"DEBUG: Socket {request.sid} is in rooms: {rooms()}")
    
    if room_id not in rooms():
        print(f"WARNING: Socket {request.sid} is NOT in room {room_id}! Re-joining...")
        join_room(room_id)
        
    emit('message', {
        'msg': content, 
        'username': current_user.username,
        'avatar_url': current_user.avatar_url 
    }, room=room_id)

@socketio.on('leave_room')
def handle_leave(data):
    print(f"DEBUG: leave_room event received: {data}")
    room_id = str(data['room_id'])
    leave_room(room_id)
    print(f"DEBUG: User {current_user.username} left room {room_id}")
    emit('message', {'msg': f'{current_user.username} has left the room', 'username': 'System'}, room=room_id)
