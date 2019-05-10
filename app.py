from flask import Flask
from flask_heroku import Heroku
import os

app = Flask(__name__)

DATABASE_DEFAULT = 'postgresql://postgres:root321@localhost/studentdb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', DATABASE_DEFAULT)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='mykeygen'

heroku = Heroku(app)

from routes import *
if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)
    