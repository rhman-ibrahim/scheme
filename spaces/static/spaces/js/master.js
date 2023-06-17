const SPACE         = document.querySelector('#space');
const SOCKET        = new WebSocket(`ws://${window.location.host}/spaces/${SPACE.dataset.serial}/`);
const BUTTON        = document.querySelector('#sendButton');

fetch(`http://${window.location.host}/spaces/${SPACE.dataset.serial}/`)
.then(response => response.json())
.then(
    data => {
        const FRAGMENT = document.createDocumentFragment();
        data.forEach(
            message => {
                Space.messageAppend(FRAGMENT, message);
            }
        );
        SPACE.append(FRAGMENT);
    }
).catch(
    error => {
        console.log(error)
    }
)


SOCKET.onerror = function(error) {
    console.error('WebSocket error:', error);
};

BUTTON.onclick = e => {
    SOCKET.send(
        JSON.stringify(
            {
                'sender': String(SPACE.dataset.username),
                'body': String(document.querySelector('#message').value)
            }
        )
    );
    document.querySelector('#message').value = '';
}

SOCKET.onmessage = e => {

    const data = JSON.parse(e.data);
    
    if (data.event === 'message') {
        Space.messageAppend(SPACE, data);
    }

    if (data.event === 'notify') {
        let notification = String(data.notification);
        if (!notification.includes(SPACE.dataset.username)) {
            let li         = document.createElement('li');
            li.textContent = `${notification}`;
            li.classList.add('notification');
            SPACE.appendChild(li);
        };
    }
}