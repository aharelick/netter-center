from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    SubmitField,
    RadioField,
    TextAreaField
)
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email
from wtforms import ValidationError
from ..models import User, Role, Tag
from .. import db


class ChangeUserEmailForm(Form):
    email = EmailField('New email', validators=[
        InputRequired(),
        Length(1, 64),
        Email()
    ])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(Form):
    role = QuerySelectField('New account type',
                            validators=[InputRequired()],
                            get_label='name',
                            query_factory=lambda: db.session.query(Role).
                            order_by('permissions'))
    submit = SubmitField('Update role')


class AdminCheckForm(Form):
    admin_check = RadioField('User Confirmed',
                             validators=[InputRequired()],
                             choices=[
                                ('y', 'Confirmed'),
                                ('n', 'Not Confirmed')])
    submit = SubmitField('Save')


class EditTagInfo(Form):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')


class NewTag(Form):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

    def validate_name(self, field):
        if Tag.query.filter_by(name=field.data).first():
            raise ValidationError('Tag name already exists.')
