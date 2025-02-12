from flask import Flask
from extensions import db
from routes.home import home_bp
from routes.hub import hub_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.about import about_bp
from routes.apps import apps_bp
from routes.admin import admin_bp

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
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
