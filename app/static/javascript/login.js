const login = async (e) => {
    e.preventDefault();

    // select the value of the login form in the browser
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value.trim();

    if (email && password) {
        // make a request to posting the new user to the database
        const response = await fetch('/api/login', {
            method: 'POST',
            body: JSON.stringify({
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
    } else {
        alert("Please enter a value for the missing fields.");
    }
    
}

document.querySelector('.input-form').addEventListener('submit', login);