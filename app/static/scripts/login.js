function submitForm() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // create an object with the data retrieved
    const formData = {
        username: username,
        email: email,
        password: password
    };

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })

    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.success) {
            showMessage("User created successfully!", 'green');
        } else {
            showMessage("User creation failed. Please try again later", 'red');
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showMessage('An error occurred. Please try again later.', 'red');
    });
}


function showMessage(message, color) {
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.innerHTML = '<p>${message}</p>';
    messageContainer.style.color = color;
} 