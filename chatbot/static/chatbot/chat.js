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

// start chat
document.querySelector("#startChatButton").addEventListener("click", () => {
    fetch('/chatbot/api/chat/start/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.conversation_id) {
            document.getElementById('chat_id').value = data.conversation_id;
            document.getElementById('current_chat_id').innerHTML = data.conversation_id;
            document.querySelector("#chatbox").innerHTML = '';
            console.log('New conversation ID:', data.conversation_id);
            
        } else {
            console.log('no new id...');
        }
    })
    .catch(error => {
        console.log('Fetch error:', error);
    });
});

// --- save chat
document.querySelector("#sendButton").addEventListener("click", async () => {
    const userInput = document.querySelector("#userInput").value;
    const chat_id = document.getElementById('chat_id').value;
    console.log('chat: ', chat_id, 'user input: ', userInput);

    fetch('/chatbot/api/chat/message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            message: userInput,
            conversation_id: chat_id 
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

// end chat
document.querySelector("#endChatButton").addEventListener("click", async () => {
    const chat_id = document.getElementById('chat_id').value;
    console.log('Ending chat id', chat_id);

    await fetch('/chatbot/end_chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({conversation_id: chat_id})
    });
    // Rest of the code...
});
