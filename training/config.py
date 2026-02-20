class Config:
    SECRET_KEY = 'you-will-never-guess-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/realtime_chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images'