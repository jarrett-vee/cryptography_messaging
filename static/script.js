function sendMessage(receiverUsername, encryptedMessage) {
    var dataToSend = {
        receiver_username: receiverUsername,
        encrypted_message: encryptedMessage
    };

    console.log("Sending data:", JSON.stringify(dataToSend));

    fetch('/messages/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
        .then(response => {
            console.log("Received raw response:", response);
            return response.json();
        })
        .then(data => {
            console.log("Parsed response data:", data);
        })
        .catch(error => {
            console.error("Error occurred:", error);
        });
}
