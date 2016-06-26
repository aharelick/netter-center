from ..decorators import admin_required

from flask import render_template, abort, redirect, flash, url_for
from flask.ext.login import login_required, current_user

from forms import (
    ChangeUserEmailForm,
    ChangeAccountTypeForm,
    AdminCheckForm,
    EditTagInfo,
    NewTag
)
from . import admin
from ..models import User, Role, Tag
from .. import db


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/registered_users.html', users=users,
                           roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'
              .format(user.full_name(), user.email),
              'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/change-account-type',
             methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'
              .format(user.full_name(), user.role.name),
              'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))


@admin.route('/user/<int:user_id>/admin-check', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_check(user_id):
    if current_user.id == user_id:
        flash('You cannot change your own administrator confirmation. Please '
              'ask another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))
    else:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404)
        form = AdminCheckForm()
        if form.validate_on_submit():
            user.admin_check = form.admin_check.data == 'y'
            db.session.add(user)
            db.session.commit()
            flash('User {}\'s confirmation status has been updated.'
                  .format(user.full_name()), 'form-success')
        else:
            form.admin_check.data = 'y' if user.admin_check else 'n'
        return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/tags')
@login_required
@admin_required
def registered_tags():
    """View all registered tags."""
    tags = Tag.query.all()
    return render_template('admin/registered_tags.html', tags=tags)


@admin.route('/tag/<int:tag_id>')
@admin.route('/tag/<int:tag_id>/info')
@login_required
@admin_required
def tag_info(tag_id):
    """View a tag's information."""
    tag = Tag.query.get(tag_id)
    if tag is None:
        abort(404)
    return render_template('admin/manage_tag.html', tag=tag)


@admin.route('/tag/<int:tag_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tag_info(tag_id):
    """Edit a tag's information."""
    tag = Tag.query.get(tag_id)
    if tag is None:
        abort(404)
    form = EditTagInfo(obj=tag)
    if form.validate_on_submit():
        form.populate_obj(tag)
        return redirect(url_for('admin.tag_info', tag_id=tag.id))
    return render_template('admin/manage_tag.html', tag=tag, form=form)


@admin.route('/tag/<int:tag_id>/delete')
@login_required
@admin_required
def delete_tag_request(tag_id):
    """Display the section with the button to delete a tag."""
    tag = Tag.query.get(tag_id)
    if tag is None:
        abort(404)
    return render_template('admin/manage_tag.html', tag=tag)


@admin.route('/tag/<int:tag_id>/_delete')
@login_required
@admin_required
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    if tag is None:
        abort(404)
    db.session.delete(tag)
    db.session.commit()
    flash('Successfully deleted tag %s.' % tag.name, 'success')
    return redirect(url_for('admin.registered_tags'))


@admin.route('/tag/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_tag():
    """Create a new tag."""
    form = NewTag()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data,
                  description=form.description.data)
        db.session.add(tag)
        db.session.commit()
        flash('%s tag successfully added.' % tag.name, 'success')
        return redirect(url_for('admin.registered_tags'))
    return render_template('admin/new_tag.html', form=form)
