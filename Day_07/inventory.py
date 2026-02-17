from flask import Flask, jsonify,request

app = Flask(__name__)

inventory = [
    {
        'item_id': 0,
        'item_name': 'Macbook Pro',
        'price': 1000000
    },
    {
        'item_id': 1,
        'item_name': 'Macbook Air',
        'price': 500000
    },
    {
        'item_id': 2,
        'item_name': 'iPhone 13',
        'price': 50000
    },
    {
        'item_id': 3,
        'item_name': 'AirPods',
        'price': 25000
    },
    {
        'item_id': 4,
        'item_name': 'iPad',
        'price': 25000
    }
]

@app.route('/')
def index():
    return "<h1>Inventory</h1>"

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)


@app.route('/inventory/<int:item_id>', methods=['POST'])
def get_item(item_id):
    return jsonify(inventory[item_id])


@app.route('/add_item', methods=['POST'])
def add_item():

    new_item = {
        'item_id': request.json['item_id'],
        'item_name': request.json['item_name'],
        'price': request.json['price']
    }
    inventory.append(new_item)
    return jsonify(new_item)

if __name__ == '__main__':
    app.run(debug=True) 