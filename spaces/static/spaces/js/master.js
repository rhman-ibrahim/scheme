let loaded       = false;

const serial     = document.querySelector('#space input[name=room]').value;
const socket     = new WebSocket(`ws://${window.location.host}/spaces/${serial}/`);
const username   = document.querySelector('#space input[name=username]').value;
const sendButton = document.querySelector('#sendButton');
const chat       = document.querySelector('#space');

function scrollToEnd () {
    if (Template.isThere('#chat li:last-child')) {
        chat.querySelector('li:last-child')
        .scrollIntoView(
            {
                behavior: "smooth",
                inline: "nearest",
                block: "start"
            }
        );
    }
}

sendButton.onclick = e => {
    let message = document.querySelector('#message').value;
    socket.send(
        JSON.stringify(
            {
                'username': username,
                'message': message
            }
        )
    );
    document.querySelector('#message').value = '';
}

socket.onmessage = e => {
    const data   = JSON.parse(e.data);
    if (data.class === 'messages' && loaded == false) {
        let fragment = document.createDocumentFragment();
        data.messages.forEach(
            message => {
                let content              = JSON.parse(message);
                let li                   = document.createElement('li');
                let usernameSpan         = document.createElement('span');
                let messageSpan          = document.createElement('span');
                li.classList.add((username == content.username) ? 'out':'in');
                usernameSpan.textContent = content.username;
                messageSpan.textContent  = content.message;
                li.appendChild(usernameSpan);
                li.appendChild(messageSpan);
                fragment.appendChild(li);
            }
        );
        chat.appendChild(fragment);
        scrollToEnd();
        loaded = true;
    }
    if (data.class === 'notice') {
        let notice = String(data.user);
        if (!notice.includes(username.value)) {
            let li         = document.createElement('li');
            li.textContent = `${notice}`;
            li.classList.add('notice');
            chat.appendChild(li);
            scrollToEnd();
        };
    }
    if (data.class === 'message') {
        let li                   = document.createElement('li');
        let usernameSpan         = document.createElement('span');
        let messageSpan          = document.createElement('span');
        li.classList.add((username == data.username) ? 'out':'in');
        usernameSpan.textContent = data.username;
        messageSpan.textContent  = data.message;
        chat.appendChild(li);
        li.appendChild(usernameSpan);
        li.appendChild(messageSpan);
        scrollToEnd();
    }
}