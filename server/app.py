from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivan:qwerty@/movies_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['CORS_ENABLED'] = False
db = SQLAlchemy(app)
login = LoginManager(app)
login.session_protection = "strong"
bcrypt = Bcrypt(app)

from routes import *

if __name__ == '__main__':
   app.run()