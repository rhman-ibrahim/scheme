const IDENTIFIER    = ROOM.get().identifier;
const SOCKET        = new WebSocket(`ws://${window.location.host}/ping/${IDENTIFIER}/`);

document.addEventListener(
    'DOMContentLoaded', 
    () => {
        fetch(
            `http://${window.location.host}/api/room/${IDENTIFIER}/messages/`,
            {
                method: 'GET',
                headers: {
                    'Authorization':`Token ${ROOM.get().token}`,
                }
            }
        )
        .then(
            response => response.json()
        )
        .then(
            data => {
                const FRAGMENT = document.createDocumentFragment();
                data.forEach(
                    message => {
                        ROOM.append(
                            FRAGMENT,
                            message
                        )
                    }
                );
                Template.append(
                    ROOM.get().ui,
                    [
                        FRAGMENT
                    ]
                )
                ROOM.scroll();
            }
        )
        .catch(error => console.log(error));
    }
)

document.getElementById('sendButton').onclick = () => {
    if (ROOM.input()) {
        SOCKET.send(ROOM.message());
        ROOM.clear();
    } 
}

SOCKET.onmessage     = received => {
    const data       = JSON.parse(received.data);
    if (data.event === 'notify') {
        Template.append(
            ROOM.get().ui,
            [
                ROOM.li(data.notification)
            ]
        );
    }
    if (data.event === 'message') {
        ROOM.append(
            ROOM.get().ui,
            data
        );
    }
}

SOCKET.onerror       = error => {
    console.error('WebSocket error:', error);
}