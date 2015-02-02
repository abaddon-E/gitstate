#-*- coding: utf-8 -*-
from project.extentions import sqldb as db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import relationship, backref
from datetime import datetime


from project.libs.date import timestamp_to_jalali
from project.libs.constants import USER_STATUS_LIST


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String(255))

    company = db.Column(db.String(120))
    established = db.Column(db.String(255))
    summary = db.Column(db.Text)
    capabilities = db.Column(db.Text)
    ceo = db.Column(db.String(255))
    phone = db.Column(db.String(64))
    fax = db.Column(db.String(64))
    address = db.Column(db.Text)

    role = db.Column(db.String(32), default='user')
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)

    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    logs = db.relationship('Log', backref='user', lazy='dynamic')
    bids = db.relationship('Bid', backref='user', lazy='dynamic')
    tenders_bids = db.relationship('TenderBid', backref='user', lazy='dynamic')

    @property
    def name(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def status(self):
        return USER_STATUS_LIST[self.active]

    @property
    def last_login_as_jalali(self):
        return timestamp_to_jalali(self.last_login)

    @property
    def phones(self):
        return self.__string_to_list(self.phone)

    def get_phones(self):
        return self.phone.split(',') if self.phone else []

    @property
    def faxes(self):
        return self.__string_to_list(self.fax)

    def get_faxes(self):
        return self.fax.split(',') if self.fax else []

    @property
    def addresses(self):
        return self.__string_to_list(self.address, '@')

    def get_addresses(self):
        return self.address.split('@') if self.address else []

    @property
    def filled_profile(self):
        return self.email and self.company and self.ceo and self.phone and self.fax and self.address

    @property
    def number_of_tenders(self):
        return len(self.tenders)

    def get_open_tenders(self):
        tenders = filter(lambda tender: tender.is_open and tender.published, self.tenders)
        return sorted(tenders, key=lambda dic: dic.id, reverse=True)

    def set_phone(self, phones_list):
        self.phone = self.__join_list(phones_list)

    def set_fax(self, faxes_list):
        self.fax = self.__join_list(faxes_list)

    def set_address(self, addresses_list):
        self.address = self.__join_list(addresses_list, '@')

    def __string_to_list(self, string, token=','):
        return ', '.join(string.split(token))

    def __join_list(self, values_list, token=','):
        return token.join(values_list)

    # Attachment's methods & properties
    @property
    def upload_dir(self):
        return current_app.config['USERS_UPLOAD_DIR']

    @property
    def __class_name_index(self):
        return class_name_id(self.__class__.__name__)

    @property
    def certificates(self):
        from project.app.attachments.models import Attachment

        return Attachment.query.filter_by(parent_id=self.id, parent_type=self.__class_name_index)
    
    def upload_files(self, files, names):
        from project.app.attachments.models import Attachment

        for index, f in enumerate(files):
            if allowed_file(f.filename):
                # replace all whitespaces with underline
                # then append it to tender_id which is directory name here
                file_name = generate_file_name(f.filename)
                upload_path = '%s%s'%(self.upload_dir, file_name)
                f.save(upload_path)

                attachment = Attachment(title=names[index], file_name=file_name,
                                        parent_id=self.id, parent_type=self.__class_name_index
                                    )
                attachment.file_type = get_file_type(upload_path)
                attachment.file_size = get_file_size(upload_path)
                
                db.session.add(attachment)
                db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def valid_password(self, password):
        return check_password_hash(self.password, password)

    def update_last_login(self):
        self.last_login = datetime.now()
        db.session.commit()

    def update_password(self, password):
        self.set_password(password)
        db.session.commit()

    @classmethod
    def load(cls, id=None):
        if id:
            return cls.query.filter_by(id=id).first_or_404()
        return cls.query.filter(cls.not_deleted(), cls.not_super_admin()).order_by(cls.id.desc())

    @classmethod
    def delete(cls,id):
        user = cls.load(id)
        user.deleted = True
        db.session.commit()
        return True

    @classmethod
    def active_users(cls):
        return cls.load().filter_by(active=True)

    @classmethod
    def super_admin(cls):
        return cls.query.filter_by(username='admin').first()

    @hybrid_method
    def not_deleted(self):
        return self.deleted == False

    @hybrid_method
    def not_super_admin(self):
        return self.username != 'admin'

    # flask-login extension needs following to work properly
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

