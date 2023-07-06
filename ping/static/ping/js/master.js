if (Template.isThere('#space')) {

    const SPACE         = document.querySelector('#space');
    const SOCKET        = new WebSocket(`ws://${window.location.host}/ping/${SPACE.dataset.serial}/`);
    const BUTTON        = document.querySelector('#sendButton');
    
    SOCKET.onerror      = function(error) {
        console.error('WebSocket error:', error);
    };
    
    BUTTON.onclick      = e => {
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
    
    SOCKET.onmessage    = e => {
        const data      = JSON.parse(e.data);
        if (data.event === 'message') {
            ConversationUI.messageAppend(SPACE, data);
        }
        if (data.event === 'notify') {
            let notification = String(data.notification);
            if (!notification.includes(SPACE.dataset.username)) {
                let li         = document.createElement('li');
                li.textContent = `${notification}`;
                li.classList.add('notification');
                ConversationUI.appendChild(li);
            };
        }
    }
    
    document.addEventListener('DOMContentLoaded', () => {
        fetch(`http://${window.location.host}/dapi/${SPACE.dataset.serial}/`)
        .then(response => response.json())
        .then(
            data => {
                const FRAGMENT = document.createDocumentFragment();
                data.forEach(
                    message => {
                        ConversationUI.messageAppend(FRAGMENT, message);
                    }
                );
                SPACE.append(FRAGMENT);
        }).catch(
            error => {
                console.log(error)
            }
        )
    })
}