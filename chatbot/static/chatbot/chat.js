document.querySelector("#sendButton").addEventListener("click", async () => {
    const userInput = document.querySelector("#userInput").value;

    // Step 1: Send message to Django server
    fetch('/chatbot/api/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')  // For Django CSRF token
        },
        body: new URLSearchParams({
            'message': userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('data', data);
        const newMessageUser = document.createElement("p");
        newMessageUser.textContent = "You: " + userInput;
        document.querySelector("#chatbox").appendChild(newMessageUser);

        const newMessageBot = document.createElement("p");
        newMessageBot.textContent = "Bot: " + data.response;
        document.querySelector("#chatbox").appendChild(newMessageBot);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Function to get the Django CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
