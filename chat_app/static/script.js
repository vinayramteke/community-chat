

document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var chatWindow = document.getElementById('chat-window'); // Reference to chat window

    socket.on('connect', function() {
        console.log('WebSocket connection established');
    });

    socket.on('disconnect', function() {
        console.log('WebSocket disconnected');
    });

    socket.on('message', function(data) {
        console.log('Message received:', data);
        displayMessage(data); // Call function to display message
    });

    // Function to display a message
    function displayMessage(data) {
        var newMessage = document.createElement('p');
        newMessage.innerHTML = '<strong>' + data.sender + ':</strong> ' + data.content;
        chatWindow.appendChild(newMessage);
    }

    // Event listener for message form submission
    document.getElementById('message-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var messageInput = document.getElementById('message-input');
        var message = messageInput.value.trim();
        if (message !== '') {
            console.log('Sending message:', message);
            socket.emit('message', message);
            messageInput.value = '';
            displayMessage({ sender: 'You', content: message }); // Display sent message immediately
        }
    });

    // Load previous messages when the page loads
    socket.emit('load_messages'); // Assuming the server has an event to request previous messages
});
