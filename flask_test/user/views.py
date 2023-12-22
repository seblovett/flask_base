# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, current_app, flash, redirect, request, url_for
from flask_login import login_required
import flask_login
from flask_test.user.models import User
from flask_test.extensions import db
from flask_test.user.forms import EditForm
from flask_test.utils import flash_errors

blueprint = Blueprint("userview", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    current_app.logger.info(User.query.all())
    us = db.session.execute(db.select(User))
    users = []
    for u in us:
        users.append(u[0])

    current_app.logger.info(users)
    return render_template("users/members.html", us=users)



@blueprint.route("/edit/<user>", methods=["GET", "POST"])
@login_required
def edit_user(user):
    """Edit a user."""
    flash(flask_login.current_user, "success")
    userdb = User.query.filter_by(username=user).first()
    form = EditForm(userdb, request.form)
    form.username.data = userdb.username
        
    if form.validate_on_submit():
        flash(f"Setting {userdb} to is_admin = {form.is_admin.data}", "success")
        userdb = userdb.update(True, active=form.active.data,email=form.email.data, is_admin=form.is_admin.data)
        userdb = User.query.filter_by(username=user).first()
        flash(f"{userdb.username} Updated!", "success")
        return redirect(url_for("userview.members"))
    else:
        flash_errors(form)
    form.email.data = userdb.email
    form.is_admin.data = userdb.is_admin
    form.active.data = userdb.active
    return render_template("users/edit.html", form=form)
