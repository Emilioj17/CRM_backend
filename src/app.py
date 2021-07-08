import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_migrate import Migrate
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
