from wtforms import Form, TextField, PasswordField, BooleanField, validators as v, \
            SubmitField, IntegerField, FileField, TextAreaField
from flask.ext.babel import lazy_gettext as _

# from models import User

min_length_msg = _('This field must be at least 3 charachter.')

class EditProfile(Form):
    email = TextField(_('Email'), [v.Required(), v.Email()])
    company = TextField(_('Company'), [v.Length(min=3, message=min_length_msg)])
    established = TextField(_('Established'))
    summary  = TextAreaField(_('Summary'))
    capabilities  = TextAreaField(_('Capabilities'))
    ceo = TextField(_('CEO'), [v.Length(min=3, message=min_length_msg)])
    phone = TextField(_('Phone'), [v.Length(min=8, max=13, message=_("this field must be between 8 and 13 charachter"))])
    fax = TextField(_('Fax'), [v.Length(min=8, max=13, message=_("this field must be between 8 and 13 charachter"))])
    address  = TextAreaField(_('Address'), [v.Length(min=3, message=min_length_msg)])
    submit = SubmitField(_('Add New User'))

class CreateUser(Form):
    email = TextField(_('Email'), [v.Required(), v.Email()])
    username = TextField(_('Username'), [v.Length(min=3, message=min_length_msg)])
    password = PasswordField(_('Password'))#, [v.EqualTo('confirm'), v.Length(min=3)])
    company = TextField(_('Company'), [v.Length(min=3, message=min_length_msg)])
    active = BooleanField(_('Active'))
    submit = SubmitField(_('Add New User'))