from flask import Blueprint, render_template, request, flash, redirect, session, url_for
import sqlite3

adminRegister_bp = Blueprint("admin_register", __name__)

# Function to add a user to database.db with SQL injection vulnerability
@adminRegister_bp.route("/admin_register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("admin_database.db")
        cursor = conn.cursor()

        # Check if username already exists
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("admin_regiter.register"))

        # VULNERABLE SQL INSERTION
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        print("Executing SQL Query:", query)  # Debugging output
        cursor.execute(query)
        conn.commit()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("admin.login"))
    
    return render_template("admin_register.html")