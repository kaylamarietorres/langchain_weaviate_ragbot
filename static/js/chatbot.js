document.addEventListener('DOMContentLoaded', (event) => {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
});