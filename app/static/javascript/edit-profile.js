const edit = async (e) => {
    const bio = document.querySelector('#bio-input').value.trim();
    const linkedin = document.querySelector('#linkedin-input').value.trim();
    const github = document.querySelector('#github-input').value.trim();

    const response = await fetch('/editProfile', {
        method: 'PUT',
        body: JSON.stringify({
            bio,
            linkedin,
            github
        }),
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
        document.location.replace('/profile')
    } else {
        alert(response.statusText);
    }
}

document.querySelector('.profile-edit-form').addEventListener('submit', edit);