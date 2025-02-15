from flask import Blueprint, render_template, request, jsonify, session
from extensions import db
from models.user import User
from models.note import Note
from datetime import datetime
from sqlalchemy import text

notes_bp = Blueprint('notes', __name__, url_prefix='/apps/notes')

@notes_bp.route('/')
def notes():
    """Render notes page with all notes"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    # VULNERABILITY: The user_id parameter is exposed and can be manipulated
    user_id = request.args.get('user_id', current_user.id)
    
    # Attempt to look like we're filtering by user_id, but allow a bypass
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        user_id = current_user.id

    all_notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    print(f"Loading notes page - Found {len(all_notes)} notes for user {user_id}")
    
    return render_template('notes.html', notes=all_notes, current_user_id=current_user.id)

@notes_bp.route('/create', methods=['POST'])
def create_note():
    """Create a new note - Intentionally vulnerable to XSS"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    title = request.form.get('title')
    content = request.form.get('content')
    
    try:
        print(f"Creating note - Title: {title}, Content: {content}")
        note = Note(
            title=title,
            content=content,
            created_at=datetime.now(),
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        print(f"Note created with ID: {note.id}")
        
        return jsonify({
            'success': True,
            'note': note.to_dict()
        })
    except Exception as e:
        print(f"Error creating note: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notes_bp.route('/search')
def search_notes():
    """Search notes with intentional SQL injection vulnerability"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    query = request.args.get('q', '')
    print(f"Search query: {query}")
    
    try:
        # Intentionally vulnerable SQL query
        sql_query = text(f"""
            SELECT id, title, content, created_at 
            FROM notes 
            WHERE title LIKE '%{query}%' 
            OR content LIKE '%{query}%'
            OR '1'='1'  -- Making the injection easier
        """)
        print(f"Executing SQL: {sql_query}")  # Debug print
        
        result = db.session.execute(sql_query)
        notes = []
        for row in result:
            try:
                created_at = row[3]
                if isinstance(created_at, str):
                    # If it's already a string, use it as is
                    created_at_str = created_at
                else:
                    # If it's a datetime object, format it
                    created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else None
                
                notes.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'created_at': created_at_str
                })
            except Exception as e:
                print(f"Error processing row {row}: {e}")
                continue
        
        print(f"Found {len(notes)} matching notes")
        return jsonify({
            'success': True,
            'notes': notes
        })
    except Exception as e:
        print(f"Error searching notes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    

@notes_bp.route('/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note with intentional access control vulnerability"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    try:
        note = Note.query.get_or_404(note_id)
        # VULNERABILITY: No check if the note belongs to the current user
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting note: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
@notes_bp.route('/debug')
def debug_database():
    """Debug route to check database contents"""
    try:
        # Check users
        users = User.query.all()
        print("\nAll Users:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}")
        
        # Check notes
        notes = Note.query.all()
        print("\nAll Notes:")
        for note in notes:
            print(f"ID: {note.id}, Title: {note.title}, User ID: {note.user_id}")
        
        # Use raw SQL to verify
        sql = text("SELECT * FROM notes")
        result = db.session.execute(sql)
        rows = result.fetchall()
        print("\nRaw SQL Notes Query Result:")
        for row in rows:
            print(row)
            
        return jsonify({
            'users': [{'id': u.id, 'username': u.username} for u in users],
            'notes': [note.to_dict() for note in notes]
        })
    except Exception as e:
        print(f"Debug Error: {e}")
        return jsonify({'error': str(e)}), 500