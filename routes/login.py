from flask import Blueprint, render_template, request, flash, redirect

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Dummy authentication
        if username == "admin" and password == "password":
            flash("Login successful!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")
