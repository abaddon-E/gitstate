'''from flask import Blueprint, render_template

from .models import User

mod = Blueprint('push_events', __name__, url_prefix='/')


@mod.route('/home')
def home():
    user = User
    return render_template('home.html', user=user)
'''
