from flask import Flask
from extensions import db
from routes.home import home_bp
from routes.hub import hub_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.about import about_bp
from routes.apps import apps_bp
from routes.notes import notes_bp
from routes.admin import admin_bp  # Import admin blueprint
from models.user import User
from models.note import Note
from models.admin import Admin  # Import admin model
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
app.register_blueprint(admin_bp)  # Register admin blueprint

def setup_database():
    """Setup database and print debug info"""
    with app.app_context():
        # Create tables only if they don't exist
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            print("No existing tables found. Creating new tables...")
            db.create_all()
            
            # Create default admin account if tables were just created
            if not Admin.query.filter_by(is_default=True).first():
                default_admin = Admin(
                    username="admin",
                    is_default=True
                )
                default_admin.set_password("password")
                db.session.add(default_admin)
                db.session.commit()
                print("Default admin account created")
        else:
            print("Existing tables found:", existing_tables)
        
        # Print schema for tables
        for table in ['notes', 'admin_credentials']:
            if table in inspector.get_table_names():
                print(f"\n{table.capitalize()} table columns:")
                for column in inspector.get_columns(table):
                    print(f"- {column['name']}: {column['type']}")
            else:
                print(f"\n{table} table does not exist!")

if __name__ == "__main__":
    setup_database()  # Call setup_database before running the app
    app.run(debug=True)