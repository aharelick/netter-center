from flask import url_for
from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField
)
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectMultipleField,
    QuerySelectField
)
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    Optional,
    URL
)
from wtforms import ValidationError
from ..models import User, Tag, UserType
from .. import db


class LoginForm(Form):
    email = EmailField('Email', validators=[
        InputRequired(),
        Length(1, 64),
        Email()
    ])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(Form):
    first_name = StringField('First name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    last_name = StringField('Last name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    email = EmailField('Email', validators=[
        InputRequired(),
        Length(1, 64),
        Email()
    ])
    password = PasswordField('Password', validators=[
        InputRequired(),
        EqualTo('password2', 'Passwords must match')
    ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    user_type = QuerySelectField('User Type',
                                 validators=[InputRequired()],
                                 get_label='name',
                                 query_factory=lambda:
                                 db.session.query(UserType))

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. (Did you mean to '
                                  '<a href="{}">log in</a> instead?)'
                                  .format(url_for('account.login')))


class RequestResetPasswordForm(Form):
    email = EmailField('Email', validators=[
        InputRequired(),
        Length(1, 64),
        Email()])
    submit = SubmitField('Reset password')

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(Form):
    email = EmailField('Email', validators=[
        InputRequired(),
        Length(1, 64),
        Email()])
    new_password = PasswordField('New password', validators=[
        InputRequired(),
        EqualTo('new_password2', 'Passwords must match.')
    ])
    new_password2 = PasswordField('Confirm new password',
                                  validators=[InputRequired()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField('New password', validators=[
        InputRequired(),
        EqualTo('new_password2', 'Passwords must match.')
    ])
    new_password2 = PasswordField('Confirm new password',
                                  validators=[InputRequired()])
    submit = SubmitField('Update password')


class ChangeEmailForm(Form):
    email = EmailField('New email', validators=[
        InputRequired(),
        Length(1, 64),
        Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class EditProfileForm(Form):
    first_name = StringField('First name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    last_name = StringField('Last name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    hometown = StringField('Hometown', validators=[
        Length(1, 64),
        Optional()
    ])
    profile_pic = URLField('Link to Profile Picture', validators=[
        URL(),
        Optional()
    ])
    bio = TextAreaField('Bio', validators=[Optional()])
    # TODO because of semantic ui, this doesn't actually query
    tags = QuerySelectMultipleField(
        'Tags',
        get_label='name',
        query_factory=lambda: db.session.query(Tag))

    submit = SubmitField('Save')
