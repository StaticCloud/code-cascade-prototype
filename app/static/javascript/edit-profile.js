let avatar = document.querySelector('img[alt="user-avatar"]').getAttribute('src')

const edit = async (e) => {
    e.preventDefault();

    const bio = document.querySelector('#bio-input').value.trim();
    const linkedin = document.querySelector('#linkedin-input').value.trim();
    const github = document.querySelector('#github-input').value.trim();

    const response = await fetch('/api/editProfile', {
        method: 'PUT',
        body: JSON.stringify({
            bio,
            linkedin,
            github,
            avatar
        }),
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
        document.location.replace('/profile')
    } else {
        alert(response.statusText);
    }
}

const selectAvatar = (e) => {
    if (e.target.hasAttribute('src')) {
        avatar = e.target.getAttribute('src')
    }

    document.querySelector('img[alt="user-avatar"]').setAttribute('src', avatar);
}

document.querySelector('.avatar-selection').addEventListener('click', selectAvatar);
document.querySelector('.profile-edit-form').addEventListener('submit', edit);