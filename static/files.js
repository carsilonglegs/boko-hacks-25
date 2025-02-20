document.addEventListener('DOMContentLoaded', function() {
    // Handle file upload form
    const form = document.getElementById('file-upload-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        fetch('/apps/files/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('File uploaded successfully');
                location.reload();
            } else {
                alert('Error uploading file: ' + data.error);
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert('Error uploading file');
        });
    });

    // Handle file deletion
    document.querySelectorAll('.delete-file').forEach(button => {
        button.addEventListener('click', function() {
            const fileId = this.getAttribute('data-file-id');
            if (confirm('Are you sure you want to delete this file?')) {
                fetch(`/apps/files/delete/${fileId}`, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('File deleted successfully');
                            location.reload();
                        } else {
                            alert('Error deleting file: ' + data.error);
                        }
                    })
                    .catch(err => {
                        console.error('Error:', err);
                        alert('Error deleting file');
                    });
            }
        });
    });
});
