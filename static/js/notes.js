// Debug mode enabled for beta testing
const DEBUG = true;

function initializeNotesApp() {
    console.log('Initializing notes app...');
    
    // Form submission
    const form = document.getElementById('note-form');
    if (form) {
        form.addEventListener('submit', saveNote);
        console.log('Form handler attached');
    }

    // Search button
    const searchButton = document.getElementById('search-button');
    if (searchButton) {
        searchButton.addEventListener('click', searchNotes);
        console.log('Search handler attached');
    }

    // Delete buttons
    document.querySelectorAll('.delete-note').forEach(button => {
        button.addEventListener('click', function() {
            const noteId = this.getAttribute('data-note-id');
            deleteNote(noteId);
        });
    });

    // Close notice
    const closeNoticeButton = document.querySelector('.close-notice');
    if (closeNoticeButton) {
        closeNoticeButton.addEventListener('click', function(e) {
            e.target.parentElement.style.display = 'none';
        });
    }
}

function saveNote(event) {
    event.preventDefault();
    console.log('Save note called');
    
    const form = document.getElementById('note-form');
    const formData = new FormData(form);

    fetch('/apps/notes/create', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            console.log('Note saved successfully');
            // Clear the form
            form.reset();
            
            // Add the new note to the display
            const notesList = document.getElementById('notes-list');
            const note = data.note;
            const noteHtml = `
                <div class="note-card">
                    <h3>${note.title}</h3>
                    <div class="note-content">${note.content}</div>
                    <div class="note-meta">
                        ID: ${note.id} | Created: ${note.created_at}
                        <button type="button" class="delete-note" data-note-id="${note.id}">Delete</button>
                    </div>
                </div>
            `;
            notesList.insertAdjacentHTML('afterbegin', noteHtml);
        }
    })
    .catch(err => {
        console.error('Save error:', err);
        alert('Error saving note. Please try again.');
    });
}

function searchNotes() {
    console.log('Search notes called');
    const query = document.getElementById('search').value;
    
    fetch(`/apps/notes/search?q=${query}`)
        .then(response => response.json())
        .then(data => {
            console.log('Search results:', data);
            const notesList = document.getElementById('notes-list');
            
            if (data.success && Array.isArray(data.notes)) {
                notesList.innerHTML = data.notes.map(note => `
                    <div class="note-card">
                        <h3>${note.title}</h3>
                        <div class="note-content">${note.content}</div>
                        <div class="note-meta">
                            ID: ${note.id} | Created: ${note.created_at}
                            <button type="button" class="delete-note" data-note-id="${note.id}">Delete</button>
                        </div>
                    </div>
                `).join('');

                // Reattach delete handlers to new notes
                document.querySelectorAll('.delete-note').forEach(button => {
                    button.addEventListener('click', function() {
                        const noteId = this.getAttribute('data-note-id');
                        deleteNote(noteId);
                    });
                });
            } else {
                // Handle error case
                notesList.innerHTML = '<div class="note-card"><p>No notes found matching your search.</p></div>';
                console.error('Search failed:', data.error);
            }
        })
        .catch(err => {
            console.error('Query error:', err);
            const notesList = document.getElementById('notes-list');
            notesList.innerHTML = '<div class="note-card"><p>An error occurred while searching notes.</p></div>';
        });
}

function deleteNote(noteId) {
    if (confirm('Delete this note?')) {
        fetch(`/apps/notes/delete/${noteId}`, { 
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                const noteElement = document.querySelector(`.note-card:has([data-note-id="${noteId}"])`);
                if(noteElement) {
                    noteElement.remove();
                }
            }
        })
        .catch(err => {
            console.error('Delete error:', err);
        });
    }
}

// Make initialization function available globally
window.initializeApp = initializeNotesApp;

// Initialize if DOM is already loaded
if (document.readyState === 'complete') {
    initializeNotesApp();
}