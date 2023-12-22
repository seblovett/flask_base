import logging
import sys

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_login import current_user
from flask_admin.contrib import sqla
from flask_test.user.models import Role
from flask_test.user.models import User as usermodel
from wtforms.fields import PasswordField
from flask_test.extensions import (
    db,
)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin
    
class UserAdmin(sqla.ModelView):

    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    def is_accessible(self):
        # return current_user.has_role('admin')
        return current_user.is_admin

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):
        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password =model.password2 #hashing of password happens in user model


class RoleAdmin(sqla.ModelView):
    def is_accessible(self):
        # return current_user.has_role('admin')
        return current_user.is_admin


def register_admin(app):
    admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4', index_view=MyAdminIndexView())
    admin.add_view(RoleAdmin(Role, db.session))
    admin.add_view(UserAdmin(usermodel, db.session, name="Users"))