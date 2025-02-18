from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admin_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert admin object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'is_default': self.is_default
        }

    def __repr__(self):
        return f'<Admin {self.username}>'