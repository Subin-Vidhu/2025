document.addEventListener('DOMContentLoaded', () => {
    fetchLinks();
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

function displayLinks(links) {
    const container = document.getElementById('links-container');
    container.innerHTML = '';

    links.forEach(link => {
        const linkElement = document.createElement('a');
        linkElement.href = link.url;
        linkElement.target = '_blank';
        linkElement.rel = 'noopener noreferrer';
        linkElement.className = 'link-item';
        linkElement.textContent = link.title;
        container.appendChild(linkElement);
    });
} 