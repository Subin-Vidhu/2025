async function fetchProfile() {
    try {
        const response = await fetch('/api/profile');
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error('Error fetching profile:', error);
    }
}

function updateUI(profile) {
    // Update profile information
    document.getElementById('avatar').src = profile.avatarUrl;
    document.getElementById('name').textContent = profile.name;
    document.getElementById('bio').textContent = profile.bio;

    // Update links
    const linksContainer = document.getElementById('links');
    linksContainer.innerHTML = ''; // Clear existing links

    profile.links.forEach(link => {
        const linkElement = document.createElement('a');
        linkElement.href = link.url;
        linkElement.target = '_blank';
        linkElement.className = 'link';
        linkElement.innerHTML = `
            <h2>${link.title}</h2>
            ${link.description ? `<p>${link.description}</p>` : ''}
        `;
        linksContainer.appendChild(linkElement);
    });
}

// Fetch profile data when page loads
document.addEventListener('DOMContentLoaded', fetchProfile);
