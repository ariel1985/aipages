/*
document.querySelector("#sendButton").addEventListener("click", () => {
    const userInput = document.querySelector("#userInput").value;
    // TODO: Send `userInput` to your chatbot and get a response
    // For now, we'll just echo the input back to the user
    const newMessage = document.createElement("p");
    newMessage.textContent = userInput;
    document.querySelector("#chatbox").appendChild(newMessage);
    console.log('the chat has been started', newMessage);
});
*/
document.querySelector("#sendButton").addEventListener("click", async () => {
    const userInput = document.querySelector("#userInput").value;

    fetch('http://localhost:5005/webhooks/rest/webhook', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sender: 'user',
            message: 'hi'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let answer = 'No answer'
        if (data && data.length > 0) {
            // Add the chatbot's response to the chatbox
             answer = data[0].text;
        }

        const newMessage = document.createElement("p");
        newMessage.textContent = answer;
        document.querySelector("#chatbox").appendChild(newMessage); 
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
