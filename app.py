from flask import Flask
from extensions import db
from routes.home import home_bp
from routes.hub import hub_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.about import about_bp
from routes.apps import apps_bp
from routes.notes import notes_bp
from models.user import User
from models.note import Note
from sqlalchemy import inspect

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boko_hacks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(hub_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(about_bp)
app.register_blueprint(apps_bp)
app.register_blueprint(notes_bp)

def setup_database():
    """Setup database and print debug info"""
    with app.app_context():
        # Create tables only if they don't exist
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            print("No existing tables found. Creating new tables...")
            db.create_all()
        else:
            print("Existing tables found:", existing_tables)
        
        # Print schema for notes table
        if 'notes' in inspector.get_table_names():
            print("\nNotes table columns:")
            for column in inspector.get_columns('notes'):
                print(f"- {column['name']}: {column['type']}")
        else:
            print("Notes table does not exist!")

if __name__ == "__main__":
    setup_database()  # Call setup_database before running the app
    app.run(debug=True)