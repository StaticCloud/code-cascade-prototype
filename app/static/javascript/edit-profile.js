let avatar = document.querySelector('img[alt="user-avatar"]').getAttribute('src')

// add selected image styling to proper icon
Array.from(document.querySelector('.avatar-selection').children).forEach(child => {
    if (child.getAttribute('src') == avatar) {
        child.classList.add('selected-avatar')
    }
})

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
    // remove selected styling from icons
    if (e.target.hasAttribute('src')) {
        Array.from(document.querySelector('.avatar-selection').children).forEach(child => {
            child.classList.add('unselected-avatar')
        })

        avatar = e.target.getAttribute('src')
        e.target.classList.remove('unselected-avatar')
        e.target.classList.add('selected-avatar')

        document.querySelector('img[alt="user-avatar"]').setAttribute('src', avatar)
    
        document.querySelector('img[alt="user-avatar"]').animate([
            {
                padding: "15px"
            },
            {
                padding: "7px"
            },
            {
                padding: "15px"
            }
        ], {
            easing: "ease-out",
            duration: 200
        }).play();
    }
}

document.querySelector('.avatar-selection').addEventListener('click', selectAvatar);
document.querySelector('.profile-edit-form').addEventListener('submit', edit);