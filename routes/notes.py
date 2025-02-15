from flask import Blueprint, render_template, request, jsonify
from extensions import db
from models.note import Note
from datetime import datetime
from sqlalchemy import or_

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
    """Search notes using SQLAlchemy"""
    query = request.args.get('q', '')
    
    try:
        # Using SQLAlchemy's query builder
        notes = Note.query.filter(
            or_(
                Note.title.like(f"%{query}%"),
                Note.content.like(f"%{query}%")
            )
        ).all()
        
        print(f"Found {len(notes)} matching notes")  # Debug print
        return jsonify({
            'success': True,
            'notes': [note.to_dict() for note in notes]
        })
    except Exception as e:
        print(f"Error searching notes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

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