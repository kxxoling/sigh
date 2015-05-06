from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin

from .models import User, Sigh


class AdminRequiredView(ModelView):
    def is_accessible(self):
        return True


def register_admin(app, db):
    admin = Admin(app, endpoint='admin', template_mode='bootstrap3')
    admin.add_view(AdminRequiredView(User, db.session))
    admin.add_view(AdminRequiredView(Sigh, db.session))

