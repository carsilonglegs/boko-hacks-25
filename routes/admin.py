from flask import Blueprint, render_template, request, flash, redirect, session, url_for, jsonify
import sqlite3
from functools import wraps
from models.user import User
from extensions import db

admin_bp = Blueprint("admin", __name__)

# Default admin credentials
DEFAULT_ADMIN = {
    "username": "admin",
    "password": "password"
}

def init_admin_db():
    """Initialize admin database with default admin account"""
    conn = sqlite3.connect("admin_database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_default INTEGER DEFAULT 0
        )
    """)
    
    # Check if default admin exists
    cursor.execute("SELECT * FROM admin_credentials WHERE is_default = 1")
    default_admin = cursor.fetchone()
    
    if not default_admin:
        cursor.execute(
            "INSERT INTO admin_credentials (username, password, is_default) VALUES (?, ?, 1)",
            (DEFAULT_ADMIN["username"], DEFAULT_ADMIN["password"])
        )
        print("Default admin account created")
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_admin_db()

def get_admin_list():
    """Get list of all admin users"""
    conn = sqlite3.connect("admin_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, is_default FROM admin_credentials")
    admins = cursor.fetchall()
    conn.close()
    return admins

@admin_bp.route("/admin-check")
def check_admin():
    """Check admin login status - used for AJAX requests"""
    is_admin = session.get('admin_logged_in', False)
    if is_admin:
        admins = get_admin_list()
        return jsonify({
            'logged_in': True,
            'is_default_admin': session.get('is_default_admin', False),
            'admins': admins
        })
    return jsonify({'logged_in': False})

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin():
    """Main admin route - handles both GET and POST requests"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = sqlite3.connect("admin_database.db")
        cursor = conn.cursor()
        
        #sql injection vulnerablity here 
        query = f"SELECT * FROM admin_credentials WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)  # This allows SQL injection

        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['is_default_admin'] = (admin[3] == 1)
            
            return jsonify({
                'success': True,
                'is_default_admin': admin[3] == 1,
                'admins': get_admin_list()
            })
        
        return jsonify({
            'success': False,
            'message': "Invalid admin credentials."
        })
    
    # For GET requests, return the admin page template
    return render_template("admin.html", 
                         admins=get_admin_list() if session.get('admin_logged_in') else None,
                         is_default_admin=session.get('is_default_admin', False))

@admin_bp.route("/admin/add", methods=["POST"])
def add_admin():
    """Add new admin user"""
    if not session.get('admin_logged_in') or not session.get('is_default_admin'):
        return jsonify({'success': False, 'message': "Unauthorized"})
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not all([username, password]):
        return jsonify({'success': False, 'message': "Missing credentials"})
    
    conn = sqlite3.connect("admin_database.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO admin_credentials (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return jsonify({
            'success': True,
            'message': "Admin added successfully",
            'admins': get_admin_list()
        })
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': "Username already exists"})
    finally:
        conn.close()

@admin_bp.route("/admin/remove/<int:admin_id>", methods=["POST"])
def remove_admin(admin_id):
    """Remove admin user"""
    if not session.get('admin_logged_in') or not session.get('is_default_admin'):
        return jsonify({'success': False, 'message': "Unauthorized"})
    
    conn = sqlite3.connect("admin_database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT is_default FROM admin_credentials WHERE id = ?", (admin_id,))
    admin = cursor.fetchone()
    
    if admin and admin[0] == 1:
        conn.close()
        return jsonify({'success': False, 'message': "Cannot remove default admin"})
    
    cursor.execute("DELETE FROM admin_credentials WHERE id = ?", (admin_id,))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': "Admin removed successfully",
        'admins': get_admin_list()
    })


@admin_bp.route("/admin/users", methods=["GET"])
def get_users():
    """Get list of all regular users"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': "Unauthorized"})
    
    try:
        users = User.query.all()
        user_list = [{
            'id': user.id, 
            'username': user.username
        } for user in users]
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({'success': False, 'message': str(e)})

@admin_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': "Unauthorized"})
    
    try:
        user = User.query.get(user_id)
        if user:
<<<<<<< HEAD
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': "User deleted successfully"})
        return jsonify({'success': False, 'message': "User not found"})
    except Exception as e:
        print(f"Error deleting user: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
=======
            # WEAK SESSION MANAGEMENT REMAINS
            session["admin_user"] = username
            return render_template("admin_hub.html")
        return render_template("admin_login.html", error="Invalid username or password")    
>>>>>>> ae4954e (creating modal for admin dashboard(troubleshooting))

@admin_bp.route("/admin/users/reset-password", methods=["POST"])
def reset_password():
    """Reset a user's password"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': "Unauthorized"})
    
    try:
        user_id = request.form.get('user_id')
        new_password = request.form.get('new_password')
        
        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            return jsonify({'success': True, 'message': "Password reset successfully"})
        return jsonify({'success': False, 'message': "User not found"})
    except Exception as e:
        print(f"Error resetting password: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

<<<<<<< HEAD
@admin_bp.route("/admin/users/add", methods=["POST"])
def add_user():
    """Add a new regular user"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': "Unauthorized"})
    
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': "Username already exists"})
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': "User added successfully",
            'user': {'id': new_user.id, 'username': new_user.username}
        })
    except Exception as e:
        print(f"Error adding user: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    


@admin_bp.route('/admin/logout', methods=['POST'])  # Make sure this endpoint exists
def logout():
    #gets rid of all admin id on log out 
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    session.pop('is_default_admin', None)
    return jsonify({"success": True, "message": "Logged out successfully"})
=======
@admin_bp.route("/admin-dashboard")
def dashboard():
    if "admin_user" in session:
        return render_template("admin_hub.html")
    return render_template("admin_login.html", error="Access denied")

@admin_bp.route("/admin-logout", methods=["POST"])
def logout():
    session.pop("admin_user", None)
    return render_template("admin_login.html")
>>>>>>> ae4954e (creating modal for admin dashboard(troubleshooting))
