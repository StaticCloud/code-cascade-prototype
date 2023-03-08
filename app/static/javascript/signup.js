const signup = async (e) => {
    e.preventDefault();

    // select the value of the sign up form in the browser
    const username = document.querySelector('input[name="username"]').value.trim();
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value.trim();

    if (username && email && password) {
        // make a request to posting the new user to the database
        const response = await fetch('/api/signup', {
            method: 'POST',
            body: JSON.stringify({
                username,
                email,
                password
            }),
            headers: { 'Content-Type': 'application/json' }
        })

        // redirect to home if the user was successfully created and authenticated
        if (response.ok) {
            document.location.replace('/')
        } else {
            alert(response.statusText);
        }
    }
    
}

document.querySelector('.auth-form').addEventListener('submit', signup);