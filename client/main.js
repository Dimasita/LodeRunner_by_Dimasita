let canvas = document.getElementById('game')
let context = canvas.getContext('2d')
let socket = new WebSocket('ws://localhost:3000')
let images = {
    back: document.getElementById('back'),
    brick: document.getElementById('brick'),
    chel: document.getElementById('chel'),
    gold: document.getElementById('gold'),
    ladder: document.getElementById('ladder'),
    me: document.getElementById('me'),
    pipe: document.getElementById('pipe'),
    wall: document.getElementById('wall')
}

socket.onmessage = function(event) {
    console.log(event)
    let board = event.data.substring(event.data.indexOf('=') + 1)
    for (let y = 0; y < 58; y++) {
        for (let x = 0; x < 58; x++) {
            let block = images.back
            switch (board[y*58 + x]) {
                case 'H':
                    block = images.ladder
                    break

                case '#':
                    block = images.brick
                    break

                case '☼':
                    block = images.wall
                    break

                case '~':
                    block = images.pipe
                    break

                case '{':
                case '}':
                case 'Y':
                case 'Я':
                case 'R':
                case '◄':
                case '►':
                case ']':
                case '[':
                    block = images.me
                    break

                case 'U':
                case ')':
                case '(':
                    block = images.chel
                    break

                case '&':
                case '@':
                case '$':
                    block = images.gold
                    break
            }

            context.drawImage(block, x*10, y*10, 10, 10)
        }
    }
}