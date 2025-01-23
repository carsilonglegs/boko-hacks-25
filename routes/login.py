from flask import Blueprint, render_template, request, flash, redirect, session, url_for

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Dummy authentication
        if username == "admin" and password == "password":
            session["user"]=username
            flash("Login successful!", "success")
            return redirect("/hub")
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)  # Remove the user from the session
    flash("You have been logged out.", "info")
    return redirect("/login")  # Redirect to the login page