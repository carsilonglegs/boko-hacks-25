from flask import Blueprint, render_template, session, redirect, url_for

hub_bp = Blueprint("hub", __name__)


@hub_bp.route("/hub")
def hub():
    # Check if user is logged in
    if "user" in session:
        return render_template("hub.html", username=session["user"])
    else:
        # Redirect to login page if not logged in
        return redirect(url_for("login.login"))
