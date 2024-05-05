const socket = io()

socket.on('connect', () => {
    socket.emit('user_logged', {data: 'User connected'})
})