from datetime import datetime
import json
from flask_cors import CORS
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_migrate import Migrate
from models import Contact, Deal, Event, Note, User, db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
from Get_Message_List import getContentMessages
from Send_Email import sendEmail

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)
app.config["JWT_SECRET_KEY"] = "@alfa123@254alfacentaurizxcvbnm@123456789ASDFGHJKL"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "username@gmail.com"
app.config['MAIL_PASSWORD'] = "password"
msg = Message()
msg.subject = "Email Subject"
msg.recipients = ['recipient@gmail.com']
msg.sender = 'username@gmail.com'
msg.body = 'Email body'
mail.send(msg)
mail = Mail(app)
jwt = JWTManager(app)


# Ruta sin usar
@app.route('/')
def main():
    return render_template('index.html')


# Ruta para Obtener Mensajes. Tipo= 'in:unread', 'is:inbox', 'in:sent'. Segun tipo, se ejecutan distintas funciones.
@app.route('/get_message', methods=['POST'])
def getMessages2():
    request_body = request.data
    decoded_object = json.loads(request_body)
    tipo = decoded_object["tipo"]
    messages = getContentMessages(tipo)
    return jsonify(messages), 201


# Ruta para Enviar email
@app.route('/enviarCorreo', methods=['POST'])
def enviar():
    request_body = request.data
    decoded_object = json.loads(request_body)
    to = decoded_object["to"]
    Cc = decoded_object["Cc"]
    subject = decoded_object["subject"]
    body = decoded_object["body"]

    sendEmail(to, Cc, subject, body)

    return jsonify("Prueba Correcta"), 201


@app.route('/login', methods=['POST'])
def login_usuario():
    request_body = request.data
    decoded_object = json.loads(request_body)
    email = decoded_object["email"]
    password = decoded_object["password"]
    user = User.query.filter(email == User.email).first()
    if user is not None and check_password_hash(user.password, password):
        token = create_access_token(identity=password)
        return jsonify(user.serialize(), token), 200
    else:
        return jsonify({"Error": "Clave o Usuario incorrecto"}), 401


@app.route('/registro', methods=['POST'])
def create_acount():
    name = request.json.get('nameReg')
    last_name = request.json.get('lastnameReg')
    phone = request.json.get('phoneReg')
    email = request.json.get('emailReg')
    password = request.json.get('passwordReg')
    create_at = datetime.now()

    user = User()
    user.name = name
    user.last_name = last_name
    user.phone = phone
    user.email = email
    user.password = password
    user.create_at = create_at

    user.save()

    return jsonify(user.serialize), 201

#@app.route('/password_reset', methods=['GET', 'POST'])
#def reset():

 #   if request.method == 'GET':
  #      return render_template('reset.html')

   # if request.method == 'POST':

    #    email = request.form.get('email')
     #   user = User.verify_email(email)

      #  if user:
       #     send_email(user)

        #return redirect(url_for('app_routes.login'))

#@app.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
#def reset_verified(token):

 #   user = User.verify_reset_token(token)
  #  if not user:
   #     print('no user found')
    #    return redirect(url_for('app_routes.login'))

    #password = request.form.get('password')
    #if password:
     #   user.set_password(password, commit=True)

      #  return redirect(url_for('app_routes.login'))

    #return render_template('reset_verified.html')


@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required()
def users(id=None):

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
        type = request.json.get('type')
        phone = request.json.get('phone')
        email = request.json.get('email')
        password = request.json.get('password')
        imgB64 = request.json.get('imgB64')
        create_at = datetime.now()

        user = User()
        user.name = name
        user.last_name = last_name
        user.rut = rut
        user.type = type
        user.phone = phone
        user.email = email
        user.password = generate_password_hash(password)
        user.imgB64 = imgB64
        user.create_at = create_at

        user.save()

        return jsonify(user.serialize()), 201

    elif request.method == 'PUT':
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        rut = request.json.get('rut')
        type = request.json.get('type')
        estado = request.json.get('estado')
        phone = request.json.get('phone')
        email = request.json.get('email')
        password = request.json.get('password')
        imgB64 = request.json.get('imgB64')

        user = User.query.get(id)
        if name != None:
            user.name = name
        if last_name != None:
            user.last_name = last_name
        if rut != None:
            user.rut = rut
        if type != None:
            user.type = type
        if estado != None:
            user.estado = estado
        if phone != None:
            user.phone = phone
        if email != None:
            user.email = email
        if password != None:
            user.password = password
        if imgB64 != None:
            user.imgB64 = imgB64

        user.update()

        return jsonify(user.serialize()), 201

    elif request.method == 'DELETE':
        user = User.query.get(id)
        user.delete()
        return jsonify({"success": "User deleted"}), 200


@app.route('/api/contacts', methods=['GET', 'POST'])
@app.route('/api/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required()
def contacts(id=None):

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

        contact = Contact.query.get(id)
        if name != None:
            contact.name = name
        if last_name != None:
            contact.last_name = last_name
        if rut != None:
            contact.rut = rut
        if type != None:
            contact.type = type
        if phone != None:
            contact.phone = phone
        if email != None:
            contact.email = email
        if user_id != None:
            contact.user_id = user_id

        contact.update()

        return jsonify(contact.serialize()), 201

    elif request.method == 'DELETE':
        contact = Contact.query.get(id)
        contact.delete()
        return jsonify({"success": "Contact deleted"}), 200


@app.route('/api/notes', methods=['GET', 'POST'])
@app.route('/api/notes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required()
def notes(id=None):

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

        note = Note.query.get(id)
        if comment != None:
            note.comment = comment
        if user_id != None:
            note.user_id = user_id
        if contact_id != None:
            note.contact_id = contact_id

        note.update()

        return jsonify(note.serialize()), 201

    elif request.method == 'DELETE':
        note = Note.query.get(id)
        note.delete()
        return jsonify({"success": "Note deleted"}), 200


@app.route('/api/events', methods=['GET', 'POST'])
@app.route('/api/events/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required()
def events(id=None):

    if request.method == 'GET':
        if id != None:
            event = Event.query.get(id)
            return jsonify(event.serialize()), 200
        else:
            events = Event.query.all()
            events = list(map(lambda event: event.serialize(), events))
            return jsonify(events), 200

    elif request.method == 'POST':
        comment = request.json.get('comment')
        create_at = datetime.now()
        date = request.json.get('date')
        date = datetime.strptime(date, '%Y-%m-%d')
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        event = Event()
        event.comment = comment
        event.create_at = create_at
        event.date = date
        event.user_id = user_id
        event.contact_id = contact_id

        event.save()

        return jsonify(event.serialize()), 201

    elif request.method == 'PUT':
        comment = request.json.get('comment')
        date = request.json.get('date')
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        event = Event.query.get(id)
        if comment != None:
            event.comment = comment
        if date != None:
            event.date = date
        if user_id != None:
            event.user_id = user_id
        if contact_id != None:
            event.contact_id = contact_id

        event.update()

        return jsonify(event.serialize()), 201

    elif request.method == 'DELETE':
        event = Event.query.get(id)
        event.delete()
        return jsonify({"success": "Note deleted"}), 200


@app.route('/api/deals', methods=['GET', 'POST'])
@app.route('/api/deals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required()
def deals(id=None):

    if request.method == 'GET':
        if id != None:
            deal = Deal.query.get(id)
            return jsonify(deal.serialize()), 200
        else:
            deals = Deal.query.all()
            deals = list(map(lambda deal: deal.serialize(), deals))
            return jsonify(deals), 200

    elif request.method == 'POST':
        plan = request.json.get('plan')
        duration = request.json.get('duration')
        description = request.json.get('description')
        create_at = datetime.now()
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        deal = Deal()
        deal.plan = plan
        deal.duration = duration
        deal.description = description
        deal.create_at = create_at
        deal.user_id = user_id
        deal.contact_id = contact_id

        deal.save()

        return jsonify(deal.serialize()), 201

    elif request.method == 'PUT':
        plan = request.json.get('plan')
        duration = request.json.get('duration')
        description = request.json.get('description')
        user_id = request.json.get('user_id')
        contact_id = request.json.get('contact_id')

        deal = Deal.query.get(id)
        if plan != None:
            deal.plan = plan
        if duration != None:
            deal.duration = duration
        if description != None:
            deal.description = description
        if user_id != None:
            deal.user_id = user_id
        if contact_id != None:
            deal.contact_id = contact_id

        deal.update()

        return jsonify(deal.serialize()), 201

    elif request.method == 'DELETE':
        deal = Deal.query.get(id)
        deal.delete()
        return jsonify({"success": "Deal deleted"}), 200


if __name__ == '__main__':
    app.run()
