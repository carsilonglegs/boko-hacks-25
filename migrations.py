#---------------------------NOTICE---------------------------#
# This file is for data base migrations and test data creation
# It will NOT be used in the final version                   #
#---------------------------NOTICE---------------------------#

from extensions import db
from models.user import User
from models.note import Note
import os

def perform_migration():
    """Recreate database with updated schema"""
    try:
        # Remove existing database
        if os.path.exists('boko_hacks.db'):
            os.remove('boko_hacks.db')
            print("Removed existing database")
        
        # Create tables with new schema
        db.create_all()
        print("Created new tables with updated schema")
        
        return True
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

def create_test_data():
    """Create test users and notes with detailed error reporting"""
    try:
        # clear out any existing data
        print("\nClearing existing data...")
        Note.query.delete()
        User.query.delete()
        db.session.commit()
        print("Existing data cleared")
        
        # Create test users
        users = [
            {"username": "alice", "password": "password123"},
            {"username": "bob", "password": "password456"},
            {"username": "charlie", "password": "password789"}
        ]
        
        print("\nCreating test users...")
        created_users = []
        for user_data in users:
            user = User(username=user_data["username"])
            user.set_password(user_data["password"])
            db.session.add(user)
            created_users.append(user)
            print(f"Added user: {user_data['username']}")
        
        db.session.commit()
        print("Users committed to database")
        
        # Verify users were created
        all_users = User.query.all()
        print(f"\nVerifying users - Found {len(all_users)} users:")
        for user in all_users:
            print(f"- ID: {user.id}, Username: {user.username}")

        # Create test notes
        notes_data = {
            "alice": [
                {"title": "Confidential Project Notes", 
                 "content": "Meeting with investors scheduled for next week. Need to prepare financial projections."},
                {"title": "Password Reminder", 
                 "content": "Admin portal: admin123 (don't share!)"}
            ],
            "bob": [
                {"title": "Development Tasks", 
                 "content": "1. Fix login bug\n2. Implement new feature\n3. Update documentation"},
                {"title": "API Keys", 
                 "content": "Production API key: sk_live_123456789"}
            ],
            "charlie": [
                {"title": "HR Meeting Notes", 
                 "content": "Discussed new hire compensation packages. Budget approved for Q3."},
                {"title": "Personal Notes", 
                 "content": "Bank account: 1234-5678-9012\nPIN: 4321"}
            ]
        }
        
        print("\nCreating test notes...")
        for user in created_users:
            print(f"\nCreating notes for {user.username}:")
            for note_data in notes_data[user.username]:
                note = Note(
                    title=note_data["title"],
                    content=note_data["content"],
                    user_id=user.id
                )
                db.session.add(note)
                print(f"- Added note: {note_data['title']}")
        
        db.session.commit()
        print("Notes committed to database")
        
        # Verify notes were created
        all_notes = Note.query.all()
        print(f"\nVerifying notes - Found {len(all_notes)} notes:")
        for note in all_notes:
            print(f"- ID: {note.id}, Title: {note.title}, User ID: {note.user_id}")
        
        return True
    except Exception as e:
        print(f"\nError creating test data: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False