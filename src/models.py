from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(100), default='Administrador')
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    imgB64 = db.Column(db.String, nullable=True)
    estado = db.Column(db.String(100), default='Activo')
    create_at = db.Column(db.DATE, nullable=False)
    contacts = db.relationship('Contact', cascade='all, delete', backref='user')
    deals = db.relationship('Deal', cascade='all, delete', backref='user')
    notes = db.relationship('Note', cascade='all, delete', backref='user')
    events = db.relationship('Event', cascade='all, delete', backref='user')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "rut": self.rut,
            "type": self.type,
            # "password": self.password,
            "estado": self.estado,
            "phone": self.phone,
            "email": self.email,
            "imgB64": self.imgB64,
            "create_at": self.formatDate(),
            "contacts": self.get_contacts(),
            "deals": self.get_deals(),
            "notes": self.get_notes(),
            "events": self.get_events()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_contacts(self):
        contacts = list(
            map(lambda contact: contact.serialize(), self.contacts))
        return contacts

    def formatDate(self):
        date = self.create_at.strftime("%d/%m/%Y")
        return date

    def get_notes(self):
        notes = list(map(lambda note: note.serialize(), self.notes))
        return notes

    def get_events(self):
        events = list(map(lambda event: event.serialize(), self.events))
        return events

    def get_deals(self):
        deals = list(map(lambda deal: deal.serialize(), self.deals))
        return deals


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    create_at = db.Column(db.DATE, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    notes = db.relationship('Note', cascade='all, delete', backref='contact')
    events = db.relationship('Event', cascade='all, delete', backref='contact')
    deals = db.relationship('Deal', cascade='all, delete', backref='contact')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "rut": self.rut,
            "type": self.type,
            "phone": self.phone,
            "email": self.email,
            "create_at": self.formatDate(),
            "user_id": self.user_id,
            "notes": self.get_notes(),
            "events": self.get_events(),
            "deals": self.get_deals()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def formatDate(self):
        date = self.create_at.strftime("%d/%m/%Y")
        return date

    def get_notes(self):
        notes = list(map(lambda note: note.serialize(), self.notes))
        return notes

    def get_events(self):
        events = list(map(lambda event: event.serialize(), self.events))
        return events

    def get_deals(self):
        deals = list(map(lambda deal: deal.serialize(), self.deals))
        return deals


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DATE, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    contact_id = db.Column(db.Integer, db.ForeignKey(
        'contacts.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "create_at": self.formatDate(),
            "user_id": self.user_id,
            "contact_id": self.contact_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def formatDate(self):
        date = self.create_at.strftime("%d/%m/%Y")
        return date


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DATE, nullable=False)
    date = db.Column(db.DATE, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    contact_id = db.Column(db.Integer, db.ForeignKey(
        'contacts.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "create_at": self.formatDate(),
            "date": self.formatDateEvent(),
            "user_id": self.user_id,
            "contact_id": self.contact_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def formatDate(self):
        date = self.create_at.strftime("%d/%m/%Y")
        return date

    def formatDateEvent(self):
        date = self.date.strftime("%d/%m/%Y")
        return date

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.String, nullable=False)
    duration = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DATE, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    contact_id = db.Column(db.Integer, db.ForeignKey(
        'contacts.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "plan": self.plan,
            "duration": self.duration,
            "description": self.description,
            "create_at": self.formatDate(),
            "user_id": self.user_id,
            "contact_id": self.contact_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def formatDate(self):
        date = self.create_at.strftime("%d/%m/%Y")
        return date
