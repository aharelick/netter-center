from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    RadioField,
    TextAreaField
)
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
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


class InviteUserForm(Form):
    role = QuerySelectField('Account type',
                            validators=[InputRequired()],
                            get_label='name',
                            query_factory=lambda: db.session.query(Role).
                            order_by('permissions'))
    first_name = StringField('First name', validators=[InputRequired(),
                                                       Length(1, 64)])
    last_name = StringField('Last name', validators=[InputRequired(),
                                                     Length(1, 64)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64),
                                            Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField('Password', validators=[
        InputRequired(), EqualTo('password2',
                                 'Passwords must match.')
    ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


class AdminCheckForm(Form):
    admin_check = RadioField('User Confirmed',
                             validators=[InputRequired()],
                             choices=[
                                ('y', 'Confirmed'),
                                ('n', 'Not Confirmed')])
    submit = SubmitField('Save')


class EditTagInfo(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description')
    submit = SubmitField('Save')


class NewTag(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

    def validate_name(self, field):
        if Tag.query.filter_by(name=field.data).first():
            raise ValidationError('Tag name already exists.')
