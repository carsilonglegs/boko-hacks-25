from flask import Blueprint, render_template, redirect, url_for, session

apps_bp = Blueprint("apps", __name__)

@apps_bp.route("/apps/<app_name>")
def load_app(app_name):
    if app_name == "notes":
        return render_template("notes.html")
    elif app_name == "upload":
        return render_template("files.html")
    elif app_name == "chat":
        return render_template("chat.html")
    elif app_name == "api":
        return render_template("api.html")
    elif app_name == "admin":
        # Return the admin template directly, the template will handle login state
        return render_template("admin.html", 
                             is_logged_in=session.get('admin_logged_in', False),
                             is_default_admin=session.get('is_default_admin', False))
    elif app_name =="admin":
        return render_template("admin_login.html")
    elif app_name == "admin_register":
        return render_template("admin_register.html")
    elif app_name == "admin-dashboard":
        return render_template("admin_hub.html")
    else:
        return "<h3>Error</h3><p>Application not found.</p>", 404