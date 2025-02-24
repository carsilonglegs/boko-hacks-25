#---------------------------NOTICE---------------------------#
# This file is for data base migrations and test data creation
# It will NOT be used in the final version                   #
#---------------------------NOTICE---------------------------#

from flask import Flask
from extensions import db
from migrations import perform_migration, create_test_data
import os

# Import all models to ensure they're registered with SQLAlchemy
from models.user import User
from models.note import Note
from routes.home import home_bp
from routes.hub import hub_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.about import about_bp
from routes.apps import apps_bp
from routes.notes import notes_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boko_hacks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(hub_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(about_bp)
app.register_blueprint(apps_bp)
app.register_blueprint(notes_bp)

if __name__ == "__main__":
    with app.app_context():
        print("\n=== Starting Database Migration ===")
        if perform_migration():
            print("\n=== Migration Successful! ===")
            print("\n=== Creating Test Data ===")
            if create_test_data():
                print("\n=== Test Data Created Successfully! ===")
                print("\nTest Users:")
                print("1. Username: alice, Password: password123")
                print("2. Username: bob, Password: password456")
                print("3. Username: charlie, Password: password789")
            else:
                print("\n=== Failed to Create Test Data! ===")
        else:
            print("\n=== Migration Failed! ===")