from blueprints.services.home.routes import home
from blueprints.services.doctors.routes import doctors
from blueprints.services.appointments.routes import appointments
from blueprints.services.feedback.routes import feedback
from blueprints.services.aiml.diagnostic.routes import diagnostic
from blueprints.services.aiml.chatbot.routes import chatbot
from blueprints.services.admin.routes import admin
from blueprints.services.dashboard.routes import dashboard
from blueprints.services.auth.routes import auth
from blueprints.services.availability.routes import availability


def init_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(doctors)
    app.register_blueprint(appointments)
    app.register_blueprint(feedback)
    app.register_blueprint(diagnostic)
    app.register_blueprint(chatbot)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(availability)