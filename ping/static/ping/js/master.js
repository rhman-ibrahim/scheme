if (Template.isThere('#room')) {

    const SERIAL        = ROOM.data().serial;
    const USERNAME      = ROOM.data().username;
    const SOCKET        = new WebSocket(`ws://${window.location.host}/ping/${SERIAL}/`);
    const BUTTON        = document.querySelector('#sendButton');
    
    SOCKET.onerror      = function(error) {
        console.error('WebSocket error:', error);
    };
    
    BUTTON.onclick      = e => {
        SOCKET.send(
            JSON.stringify(
                {
                    'sender': String(USERNAME),
                    'body': String(document.querySelector('#message').value)
                }
            )
        );
        document.querySelector('#message').value = '';
    }
    
    SOCKET.onmessage    = e => {
        const data      = JSON.parse(e.data);
        if (data.event === 'message') {
            ROOM.messageAppend(ROOM.UI(), data);
        }
        if (data.event === 'notify') {
            let notification = String(data.notification);
            if (!notification.includes(USERNAME)) {
                let li         = document.createElement('li');
                li.textContent = `${notification}`;
                li.classList.add('notification');
                ROOM.appendChild(li);
            };
        }
    }
    
    document.addEventListener('DOMContentLoaded', () => {
        fetch(`http://${window.location.host}/dapi/${SERIAL}/`)
        .then(response => response.json())
        .then(
            data => {
                const FRAGMENT = document.createDocumentFragment();
                data.forEach(message => ROOM.messageAppend(FRAGMENT, message));
                ROOM.UI().append(FRAGMENT);
            }
        ).catch(error => console.log(error));
    })
}