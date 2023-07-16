class ROOM {
    static UI = () => {
        return document.querySelector('#room');
    }
    static data = () => {
        return {
            username: document.getElementById('room-input_button-container').dataset.username,
            serial: document.getElementById('room').dataset.serial,
        };
    }
    static fixChatBoxWidth = () => {
        if (Template.isThere('#room')) {
            const BOX       = document.querySelector('#room-input_button-container');
            BOX.style.width = `${BOX.parentElement.offsetWidth}px`;
        }
    }
    static messageUlElement = (destination, data) => {
        let ulElement          = document.createElement('ul');
        let mLiElement         = document.createElement('li');
        let uLiElement         = document.createElement('li');
        uLiElement.textContent = data.sender;
        mLiElement.textContent = data.body;
        ulElement.appendChild(uLiElement);
        ulElement.appendChild(mLiElement);
        ulElement.setAttribute(
            'data-direction', (document.querySelector('#room').dataset.username == data.sender) ? 'out':'in'
        );
        ulElement.setAttribute(
            'data-sender', data.sender
        );
        destination.appendChild(ulElement);
    }
    static messageLiElement = (destination, data) => {
        let liElement         = document.createElement('li');
        liElement.textContent = data.body;
        destination.querySelector('ul:last-of-type').appendChild(liElement);
    }
    static messageAppend = (destination, data) => {
        if (
            destination.querySelector('ul:last-of-type') &&
            destination.querySelector('ul:last-of-type').dataset.sender == data.sender
        ) {
            ROOM.messageLiElement(destination, data);
        } else {
            ROOM.messageUlElement(destination, data);
        }
        ROOM.scrollToDestination(destination);
    }
    static scrollToDestination = destination => {
        destination.querySelector('ul:last-of-type').scrollIntoView(
            {
                block: 'start',
                inline: 'nearest',
                behavior:'smooth',
            }
        );
    }
}