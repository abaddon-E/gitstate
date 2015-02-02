'''#-*- coding: utf-8 -*-
from project.extensions import db
from flask import render_template, request, redirect, url_for, flash, session
from flask import current_app as app
from flask.ext.login import login_required, current_user
from flask.ext.babel import lazy_gettext as _

from ..forms import EditProfile
from project.app.auth.forms import ChangePassword
from project.libs.decorators import check_current_user_is
from project.app.tenders.models import Tender
from . import mod


@mod.route('/dashboard/', methods=['GET'])
@mod.route('/dashboard/page:<int:page>/', methods=['GET'])
@login_required
@check_current_user_is('user')
def dashboard(page=1):
    tenders = Tender.get_user_tenders(current_user).order_by(Tender.id.desc())

    tenders_count = tenders.count()
    tenders = tenders.paginate(page, per_page=app.config['PER_PAGE'], error_out=True)

    return render_template('users/frontend/dashboard.html', tenders=tenders, tenders_count=tenders_count)

@mod.route('/change_password/', methods=['GET', 'POST'])
@login_required
@check_current_user_is('user')
def change_password():
    form = ChangePassword(request.form)

    if request.method == 'POST' and form.validate():
        if current_user.valid_password(request.form['password']):
            current_user.update_password(request.form.get('new_password'))

            flash(unicode(_('Password has been changed.')))
            return redirect(url_for('users.change_password'))

        flash(_('Password is not correct.'))

    return render_template('users/frontend/change_password.html', form=form)


@mod.route('/profile/edit/', methods=['GET', 'POST'])
@login_required
@check_current_user_is('user')
def edit_profile():
    user = current_user
    form = EditProfile(request.form, obj=user)

    if request.method == 'POST' and form.validate():
        if request.files.get('certificates'):
                user.upload_files(request.files.getlist('certificates'),
                            request.form.getlist('certificates_title'))

        form.populate_obj(user)
        user.set_fax(request.form.getlist('fax'))
        user.set_phone(request.form.getlist('phone'))
        user.set_address(request.form.getlist('address'))

        db.session.commit()

        flash( unicode(_('Profile has updated.')) )
        return redirect(url_for('users.edit_profile'))

    title = form.submit.label.text = _('Update User')
    action = url_for('users.edit_profile')
    return render_template('users/frontend/edit_profile.html', form=form, action=action, user=user, title=title)

'''
