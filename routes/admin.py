from flask import Blueprint, render_template, request, flash, redirect, session, url_for
import sqlite3

admin_bp = Blueprint("admin", __name__)

def initialize_admin_database():
    conn = sqlite3.connect("admin_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database when the app starts
initialize_admin_database()

@admin_bp.route("/admin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # SQL INJECTION VULNERABILITY ALLOWS BYPASS
        conn = sqlite3.connect("admin_database.db")
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}' OR '1'='1'"
        cursor.execute(query)  # Directly using user input in SQL
        user = cursor.fetchone()
        conn.close()

        if user:
            # WEAK SESSION MANAGEMENT REMAINS
            session["admin_user"] = username
            flash("Admin login successful!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("admin_login.html")

@admin_bp.route("/admin-dashboard")
def dashboard():
    if "admin_user" in session:
        return render_template("admin_hub.html")
    return redirect(url_for("admin.login"))
