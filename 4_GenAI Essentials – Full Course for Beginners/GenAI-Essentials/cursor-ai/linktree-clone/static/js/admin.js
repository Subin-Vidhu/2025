document.addEventListener('DOMContentLoaded', () => {
    fetchLinks();
    setupFormHandler();
});

async function fetchLinks() {
    try {
        const response = await fetch('/api/links');
        const links = await response.json();
        displayLinks(links);
    } catch (error) {
        console.error('Error fetching links:', error);
    }
}

function setupFormHandler() {
    const form = document.getElementById('add-link-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = document.getElementById('title').value;
        const url = document.getElementById('url').value;

        try {
            const response = await fetch('/api/links', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, url }),
            });

            if (response.ok) {
                form.reset();
                fetchLinks();
            } else {
                const error = await response.json();
                alert(error.error || 'Failed to add link');
            }
        } catch (error) {
            console.error('Error adding link:', error);
            alert('Failed to add link');
        }
    });
}

function displayLinks(links) {
    const container = document.getElementById('links-container');
    container.innerHTML = '';

    links.forEach(link => {
        const linkElement = document.createElement('div');
        linkElement.className = 'link-item';
        linkElement.innerHTML = `
            <div class="link-info">
                <strong>${link.title}</strong>
                <small>${link.url}</small>
            </div>
            <div class="actions">
                <button onclick="deleteLink('${link.id}')" class="delete-btn">Delete</button>
            </div>
        `;
        container.appendChild(linkElement);
    });
}

async function deleteLink(id) {
    if (!confirm('Are you sure you want to delete this link?')) {
        return;
    }

    try {
        const response = await fetch(`/api/links/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            fetchLinks();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to delete link');
        }
    } catch (error) {
        console.error('Error deleting link:', error);
        alert('Failed to delete link');
    }
} 