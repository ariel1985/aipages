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

function start_chat() {
    return fetch('/chatbot/api/chat/start/', {
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
        if(data.chat_id) {
            document.getElementById('chat_id').value = data.chat_id;
            document.getElementById('current_chat_id').innerHTML = data.chat_id;
            document.querySelector("#chatbox").innerHTML = '';
            console.log('New chat ID:', data.chat_id);
            return data.chat_id;
        } else {
            console.log('no new id...');
            return null;
        }
    });
}


async function save_chat() {
    const userInput = document.querySelector("#userInput").value;
    let chat_id = document.getElementById('chat_id').value;

    if (!chat_id) {
        chat_id = await start_chat(); // Here, you wait for the Promise to resolve and get the chat_id
    }
    console.log('Edited chat_id', chat_id);

    fetch('/chatbot/api/chat/message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            message: userInput,
            chat_id: chat_id
        })
    })
    .then(response => response.json())
    .then(data => {
        const newMessageUser = document.createElement("p");
        newMessageUser.textContent = "You: " + userInput;
        document.querySelector("#chatbox").appendChild(newMessageUser);

        const newMessageBot = document.createElement("p");
        newMessageBot.textContent = "Bot: " + data.response;
        document.querySelector("#chatbox").appendChild(newMessageBot);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function end_chat() {
    const chat_id = document.getElementById('chat_id').value;

    fetch('/chatbot/api/chat/end/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({chat_id: chat_id})
    })
    .then(data => {
        if (data.ok) 
            console.log('Chat has ended...', data);
        else 
            console.log('No good... no end to the chat');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.querySelector("#startChatButton").addEventListener("click", start_chat);
document.querySelector("#sendButton").addEventListener("click", save_chat);
document.querySelector("#endChatButton").addEventListener("click", end_chat);



// After your existing JavaScript functions:

function populate_chat(chat_data) {
    const chatbox = document.querySelector("#chatbox");
    chat_data.forEach(message => {
        const msgElement = document.createElement("p");
        msgElement.textContent = message.user + ": " + message.content;
        chatbox.appendChild(msgElement);
    });
}

