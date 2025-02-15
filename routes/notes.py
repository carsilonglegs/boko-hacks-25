from flask import Blueprint, render_template, request, jsonify
from extensions import db
from models.note import Note
from datetime import datetime
from sqlalchemy import text

notes_bp = Blueprint('notes', __name__, url_prefix='/apps/notes')

@notes_bp.route('/')
def notes():
    """Render notes page with all notes"""
    all_notes = Note.query.order_by(Note.created_at.desc()).all()
    print(f"Loading notes page - Found {len(all_notes)} notes")  # Debug print
    for note in all_notes:
        print(f"Note {note.id}: {note.title}")  # Debug print
    return render_template('notes.html', notes=all_notes)

@notes_bp.route('/create', methods=['POST'])
def create_note():
    """Create a new note - Intentionally vulnerable to XSS"""
    title = request.form.get('title')
    content = request.form.get('content')
    
    try:
        print(f"Creating note - Title: {title}, Content: {content}")  # Debug print
        note = Note(
            title=title,  # No sanitization
            content=content,  # No sanitization
            created_at=datetime.now()
        )
        db.session.add(note)
        db.session.commit()
        print(f"Note created with ID: {note.id}")  # Debug print
        
        return jsonify({
            'success': True,
            'note': note.to_dict()
        })
    except Exception as e:
        print(f"Error creating note: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notes_bp.route('/search')
def search_notes():
    """Search notes - Intentionally vulnerable to SQL injection"""
    query = request.args.get('q', '')
    
    try:
        # WARNING: This is intentionally vulnerable to SQL injection
        sql = text(f"SELECT * FROM notes WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'")
        result = db.session.execute(sql)
        
        notes = [
            {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'created_at': row[3].strftime('%Y-%m-%d %H:%M:%S')
            }
            for row in result
        ]
        
        return jsonify({'notes': notes})
    except Exception as e:
        print(f"Error searching notes: {e}")
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting note: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500