from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import resend
import os 


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    class ResendHandler(logging.Handler):
        def emit(self, record):
            resend.api_key = app.config['RESEND_API_KEY']
            resend.Emails.send({
                "from": app.config['MAIL_SENDER'],
                "to": app.config['ADMINS'],
                "subject": "Microblog Failure",
                "text": self.format(record)
            })

    mail_handler = ResendHandler()
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


    
from app import routes, models, errors