from flask import render_template, redirect, url_for
from flask.ext.login import current_user
from . import main


@main.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('account.my_profile'))
    else:
        return render_template('main/homepage.html')

