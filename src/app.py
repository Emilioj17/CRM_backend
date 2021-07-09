from datetime import datetime
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_migrate import Migrate
from models import User, db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users(id = None):

    if request.method == 'GET':
        if id != None:
            user = User.query.get(id)
            return jsonify(user.serialize()), 200
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users.serialize()), 200
    elif request.method == 'POST':
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        phone = request.json.get('phone')
        email = request.json.get('email')
        create_at = datetime.datetime.now()

        user = User()
        user.name = name
        user.last_name = last_name
        user.phone = phone
        user.email = email
        user.create_at = create_at

        user.save()

        return jsonify(user.serialize()), 201
    


if __name__ == '__main__':
    app.run()
