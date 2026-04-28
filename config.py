import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "sqlite:///" + os.path.join(basedir, 'app.db')
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    ADMINS = os.environ.get('ADMINS', '').split(',')