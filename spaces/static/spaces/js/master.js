const SPACE         = document.querySelector('#space');
const SERIAL        = document.querySelector('#space input[name=room]').value;
const USERNAME      = document.querySelector('#space input[name=username]').value;

const SOCKET        = new WebSocket(`ws://${window.location.host}/spaces/${SERIAL}/`);
const BUTTON        = document.querySelector('#sendButton');

let load_event_flag = false;


function messageUlElement (destination, data) {
    let ulElement          = document.createElement('ul');
    let mLiElement         = document.createElement('li');
    let uLiElement         = document.createElement('li');
    uLiElement.textContent = data.sender;
    mLiElement.textContent = data.body;
    ulElement.appendChild(uLiElement);
    ulElement.appendChild(mLiElement);
    ulElement.setAttribute('data-direction', (USERNAME == data.sender) ? 'out':'in');
    ulElement.setAttribute('data-sender', data.sender);
    destination.appendChild(ulElement);
}

function messageLiElement(destination, data) {
    let liElement         = document.createElement('li');
    liElement.textContent = data.body;
    destination.querySelector('ul:last-of-type').appendChild(liElement);
}

function messageAppend (destination, data) {
    if (
        destination.querySelector('ul:last-of-type') &&
        destination.querySelector('ul:last-of-type').dataset.sender == data.sender
    ) {
        messageLiElement(destination, data);
    } else {
        messageUlElement(destination, data);
    }
}


BUTTON.onclick = e => {
    SOCKET.send(
        JSON.stringify(
            {
                'username': String(USERNAME),
                'message': String(document.querySelector('#message').value)
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
                messageAppend(FRAGMENT, JSON.parse(message));
            }
        );
        SPACE.append(FRAGMENT);
        load_event_flag = true;
    }

    if (data.event === 'message') {
        messageAppend(SPACE, data);
    }

    if (data.event === 'notify') {
        let notification = String(data.user);
        if (!notification.includes(USERNAME)) {
            let li         = document.createElement('li');
            li.textContent = `${notification}`;
            li.classList.add('notification');
            SPACE.appendChild(li);
        };
    }
}