async function save_chat_with_button() {
    console.log('in chat with button');
    const userInput2 = document.querySelector("#userInput2").value;
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
            message: userInput2,
            chat_id: chat_id
        })
    })
    .then(response => response.json()) 
    .then(data => {
        console.log('COMPLEX data HERE', data);
        const chatbox = document.querySelector("#chatbox");
        
        // User
        const newMessageUser = document.createElement("p");
        newMessageUser.textContent = "You: " + userInput2;
        chatbox.appendChild(newMessageUser);

        // BOT - is more complex
        console.log('data length', data['rasa_data'].length);
        
        if (data['rasa_data'].length > 0 ) {
            for (let i = 0; i < data['rasa_data'].length; i++) {
                const elm = data['rasa_data'][i];
                console.log(elm);
                // text
                if (elm.text) {
                    console.log(elm.text);
                    chatbox.appendChild(text_elm(elm.text));
                }
                
                // image
                if (elm.image) {
                    console.log(elm.image);
                    chatbox.appendChild(image_elm(elm.image));
                }
                // button
                if (elm.buttons) {
                    console.log('its a BUTTON', elm.buttons.length, elm.buttons);
                    for (let j = 0; j < elm.buttons.length; j++) {
                        const btn = elm.buttons[j];
                        console.log(btn);
                        chatbox.appendChild(button_elm(btn.title, btn.payload));
                        
                    }
                }
            }
        }
        else {
            chatbox.appendChild(text_elm('No answer :( '));
        }

        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function button_elm(text, payload) {
    const newMessageBot = document.createElement("p");
    const btn = document.createElement('button');
    
    btn.innerHTML = text;
    btn.addEventListener('click', () => payload_handler(payload));
    
    newMessageBot.appendChild(btn);
    return newMessageBot;
}

// Example external function
function payload_handler(data) {
    console.log('Button clicked with payload:', data);
}


function text_elm(text) {
    const newMessageBot = document.createElement("p");
    newMessageBot.textContent = "Bot: " + text;
    return newMessageBot
}

function image_elm(src) {
    const newMessageBot = document.createElement("img");
    newMessageBot.style.height = '70%';
    newMessageBot.src = src;
    return newMessageBot
}


function handleEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // To prevent any default behavior associated with the Enter key
        save_chat_with_button();
    }
}
document.querySelector("#userInput2").addEventListener("keyup", handleEnter);
document.querySelector("#sendButton2").addEventListener("click", save_chat_with_button);