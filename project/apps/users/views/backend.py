'''#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import login_required

from project.extentions import sqldb as db
from project.libs.decorators import check_current_user_is
from project.libs.constants import USER_STATUS_LIST
from project.app.tenders.models import Tender
from ..forms import CreateUser
from ..models import User
from . import mod

@mod.route('/admin_dashboard/')
@login_required
@check_current_user_is('admin')
def admin_dashboard():
    open_tenders = Tender.open_tenders()
    return render_template('users/backend/dashboard.html',
            number_of_active_users = User.active_users().count(),
            number_of_users = User.load().count(),
            number_of_open_tenders=open_tenders.count(),
            number_of_tenders= Tender.load().count(),
            open_tenders=open_tenders
        )

@mod.route('/')
@login_required
@check_current_user_is('admin')
def index():
    status_list = [(id, _(value)) for id, value in enumerate(USER_STATUS_LIST)]
    users = User.load()

    if request.args.get('status'):
        status = True if int(request.args.get('status')) else False
        users = users.filter_by(active=status)

    return render_template('users/backend/index.html', users=users, status_list=status_list)

@mod.route('/<int:id>/show/')
@login_required
@check_current_user_is('admin')
def show(id):
    user = User.load(id)
    user_tenders = Tender.get_user_tenders(user).order_by(Tender.id.desc())
    return render_template('users/backend/show.html', user=user, tenders=user_tenders)

@mod.route('/create/', methods=['GET', 'POST'])
@login_required
@check_current_user_is('admin')
def create():
    form = CreateUser(request.form)

    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        user.set_password(request.form['password'])

        db.session.add(user)
        db.session.commit()

        flash(unicode(_('New user added.')))
        return redirect(url_for('users.index'))

    title = _('Add New User')
    action = url_for('users.create')
    return render_template('users/backend/create.html', form=form, action=action, title=title)


@mod.route('/<int:id>/update/', methods=['GET', 'POST'])
@login_required
@check_current_user_is('admin')
def update(id):
    user = User.load(id)
    form = CreateUser(request.form, obj=user)

    if request.method == 'POST' and form.validate():
        if request.form['password']:
            user.set_password(request.form['password'])

        form.password.data = user.password
        form.populate_obj(user)

        db.session.commit()
        flash('User updated.')
        return redirect(url_for('users.index'))

    form.password.data = None
    title = form.submit.label.text = _('Update User')
    action = url_for('users.update', id=id)
    return render_template('users/backend/create.html', form=form, action=action, user=user, title=title)


@mod.route('/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
@check_current_user_is('admin')
def delete(id):
    User.delete(id)
    return redirect(url_for('users.index'))

@mod.route('/print/')
@login_required
@check_current_user_is('admin')
def print_list():
    return render_template('users/backend/print_list.html', users=User.load())

@mod.route('/search/')
@login_required
@check_current_user_is('admin')
def search():
    result = User.query

    if request.args.get('keyword'):
        keyword = '%{0}%'.format(request.args.get('keyword').strip())
        result = result.filter(
                User.username.ilike(keyword) | User.email.ilike(keyword) | User.address.ilike(keyword) |
                User.phone.ilike(keyword) | User.fax.ilike(keyword) | User.ceo.ilike(keyword) |
                User.company.ilike(keyword)
            )

    return render_template('users/backend/index.html', users=result)

@mod.route('/check_form/', methods=['POST'])
@login_required
@check_current_user_is('admin')
def check_form():
    result = {'username': 'valid', 'email': 'valid'}

    username = User.query.filter_by(username=request.form['username'], deleted=False).first()
    if(username):
        result['username'] = 'not_valid'

    email = User.query.filter_by(email=request.form['email'], deleted=False).first()
    if(email):
        result['email'] = 'not_valid'

    return jsonify( { 'result': result } )
'''
