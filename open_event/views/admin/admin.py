"""Copyright 2015 Rafal Kowalski"""
from flask.ext import login
from flask_admin import Admin

from open_event.models import db
from open_event.models.event import Event
from open_event.models.role import Role
from open_event.models.user import User
from open_event.views.admin.models_views.events import EventsView
from open_event.views.admin.models_views.roles import RoleView
from open_event.views.admin.models_views.profile import ProfileView
from open_event.views.admin.home import MyHomeView



class AdminView(object):
    """Main Admin class View"""
    def __init__(self, app_name):
        self.admin = Admin(name=app_name, template_mode='bootstrap3', index_view=MyHomeView())

    def init(self, app):
        """Init flask admin"""
        self.admin.init_app(app)
        self._add_views()

    def _add_views(self):
        events = EventsView(Event, db.session, name='Events', url='events')
        self.admin.add_view(events)
        self.admin.add_view(RoleView(Role, db.session, name='Role', url='events/<event_id>/roles'))

        profile = ProfileView(User, db.session, name='Profile', url='profile')

        # self.admin.add_view(ev)
        self.admin.add_view(events)
        self.admin.add_view(profile)

    @staticmethod
    def init_login(app):
        """Init login"""
        login_manager = login.LoginManager()
        login_manager.init_app(app)

        # Create user loader function
        @login_manager.user_loader
        def load_user(user_id):
            return db.session.query(User).get(user_id)

