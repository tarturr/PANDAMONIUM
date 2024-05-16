const socket = io()

socket.on('connect', () => {
    socket.emit('user_logged', {data: 'User connected'})
})

const messages = document.querySelector('.messages')
const chatBox = document.getElementById('chatbox')
const sendButton = document.getElementById('send')

sendButton.addEventListener('click', (e) => {
    const message = chatBox.value.trim()
    console.log(message)

    if (message.length > 0) {
        socket.emit('user_message', {data: message})
    }
})

socket.on('user_message', (data) => {
    const message = document.createElement('p')
    message.textContent = data['data']
    messages.appendChild(message)
})