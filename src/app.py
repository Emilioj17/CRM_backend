from datetime import datetime
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_migrate import Migrate
from models import Contact, Deal, Note, User, db

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
            return jsonify(users), 200
            
    elif request.method == 'POST':
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        rut = request.json.get('rut')
        phone = request.json.get('phone')
        email = request.json.get('email')
        create_at = datetime.now()

        user = User()
        user.name = name
        user.last_name = last_name
        user.rut = rut
        user.phone = phone
        user.email = email
        user.create_at = create_at



        user.save()

        return jsonify(user.serialize()), 201
    elif request.method == 'PUT':
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        rut = request.json.get('rut')
        phone = request.json.get('phone')
        email = request.json.get('email')

        user = User()
        user.name = name
        user.last_name = last_name
        user.rut = rut
        user.phone = phone
        user.email = email

        user.update()

        return jsonify(user.serialize()), 201
    elif request.method == 'DELETE':
        user = User.query.get(id)
        user.delete()
        return jsonify({ "success": "User deleted"}), 200
    

@app.route('/api/contacts', methods=['GET', 'POST'])
@app.route('/api/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def contacts(id = None):

    if request.method == 'GET':
        if id != None:
            contact = Contact.query.get(id)
            return jsonify(contact.serialize()), 200
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200

    elif request.method == 'POST':
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        rut = request.json.get('rut')
        type = request.json.get('type')
        phone = request.json.get('phone')
        email = request.json.get('email')
        create_at = datetime.now()
        user_id = request.json.get('user_id')

        contact = Contact()
        contact.name = name
        contact.last_name = last_name
        contact.rut = rut
        contact.type = type
        contact.phone = phone
        contact.email = email
        contact.create_at = create_at
        contact.user_id = user_id

        contact.save()

        return jsonify(contact.serialize()), 201

    elif request.method == 'PUT':
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        rut = request.json.get('rut')
        type = request.json.get('type')
        phone = request.json.get('phone')
        email = request.json.get('email')
        user_id = request.json.get('user_id')

        contact = Contact()
        contact.name = name
        contact.last_name = last_name
        contact.rut = rut
        contact.type = type
        contact.phone = phone
        contact.email = email
        contact.user_id = user_id

        contact.update()

        return jsonify(contact.serialize()), 201

    elif request.method == 'DELETE':
        contact = Contact.query.get(id)
        contact.delete()
        return jsonify({ "success": "Contact deleted"}), 200


@app.route('/api/notes', methods=['GET', 'POST'])
@app.route('/api/notes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def notes(id = None):
    
    if request.method == 'GET':
        if id != None:
            note = Note.query.get(id)
            return jsonify(note.serialize()), 200
        else:
            notes = Note.query.all()
            notes = list(map(lambda note: note.serialize(), notes))
            return jsonify(notes), 200

    elif request.method == 'POST':
        comment = request.json.get('comment')
        create_at = datetime.now()
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        note = Note()
        note.comment = comment
        note.create_at = create_at
        note.user_id = user_id
        note.contact_id = contact_id

        note.save()

        return jsonify(note.serialize()), 201

    elif request.method == 'PUT':
        comment = request.json.get('comment')
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        note = Note()
        note.comment = comment
        note.user_id = user_id
        note.contact_id = contact_id

        note.update()

        return jsonify(note.serialize()), 201

    elif request.method == 'DELETE':
        note = Note.query.get(id)
        note.delete()
        return jsonify({ "success": "Note deleted"}), 200


@app.route('/api/deals', methods=['GET', 'POST'])
@app.route('/api/deals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def deals(id = None):
    
    if request.method == 'GET':
        if id != None:
            deal = Deal.query.get(id)
            return jsonify(deal.serialize()), 200
        else:
            deals = Note.query.all()
            deals = list(map(lambda deal: deal.serialize(), deals))
            return jsonify(deals), 200

    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        create_at = datetime.now()
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        deal = Deal()
        deal.name = name
        deal.description = description
        deal.create_at = create_at
        deal.user_id = user_id
        deal.contact_id = contact_id

        deal.save()

        return jsonify(deal.serialize()), 201

    elif request.method == 'PUT':
        name = request.json.get('name')
        description = request.json.get('description')
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        deal = Deal()
        deal.name = name
        deal.description = description
        deal.user_id = user_id
        deal.contact_id = contact_id

        deal.update()

        return jsonify(deal.serialize()), 201

    elif request.method == 'DELETE':
        deal = Deal.query.get(id)
        deal.delete()
        return jsonify({ "success": "Deal deleted"}), 200

if __name__ == '__main__':
    app.run()
