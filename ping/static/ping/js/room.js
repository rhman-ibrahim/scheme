const SERIAL        = ROOM.get().serial;
const SOCKET        = new WebSocket(`ws://${window.location.host}/ping/${SERIAL}/`);

document.addEventListener(
    'DOMContentLoaded', 
    () => {
        fetch(`http://${window.location.host}/dapi/${SERIAL}/`)
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
                    ROOM.get().conversation,
                    [
                        FRAGMENT
                    ]
                )
                ROOM.scroll();
            }
        )
        .catch(
            error => console.log(error)
        );
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
            ROOM.get().conversation,
            [
                ROOM.li(data.notification)
            ]
        );
    }
    if (data.event === 'message') {
        ROOM.append(
            ROOM.get().conversation,
            data
        );
    }
}

SOCKET.onerror       = error => {
    console.error('WebSocket error:', error);
}