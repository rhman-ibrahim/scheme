const SPACE         = document.querySelector('#space');
const SOCKET        = new WebSocket(`ws://${window.location.host}/spaces/${SPACE.dataset.serial}/`);
const BUTTON        = document.querySelector('#sendButton');
let load_event_flag = false;

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
    
    if (data.event === 'load' && load_event_flag == false) {
        const FRAGMENT = document.createDocumentFragment();
        data.messages.forEach(
            message => {
                Space.messageAppend(FRAGMENT, JSON.parse(message));
            }
        );
        SPACE.append(FRAGMENT);
        load_event_flag = true;
    }

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