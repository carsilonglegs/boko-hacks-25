from flask import Flask
from routes.home import home_bp
from routes.hub import hub_bp
from routes.login import login_bp



app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(hub_bp)
app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(debug=True)
