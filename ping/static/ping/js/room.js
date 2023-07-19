class ROOM {
    
    static get = () => {
        return {
            serial: String(document.getElementById('room').dataset.serial),
            username: String(document.getElementById('room-input').dataset.username),
            message: String(document.getElementById('message').value),
            last: document.getElementById('room').querySelector('ul:last-of-type'),
            conversation: document.querySelector('#room'),
        };
    }

    static input = () => {
        if (ROOM.get().message.trim().length !== 0) return true;
        return false;
    }

    static message = () => {
        return JSON.stringify(
            {
                'sender': ROOM.get().username,
                'body': ROOM.get().message
            }
        )
    }

    static li = text => {
        const li       = document.createElement('li');
        li.textContent = String(text);
        return li;
    }

    static ul = data => {
        const ul = document.createElement('ul');
        const dr = (ROOM.get().username == data.sender) ? 'outgoing':'incoming';
        ul.setAttribute('class', dr);
        return ul;
    }

    static appendLi = (destination, data) => {
        destination.querySelector('ul:last-of-type').appendChild(ROOM.li(data.body));
    }

    static appendUl = (destination, data) => {
        destination.appendChild(
            Template.append(
                ROOM.ul(data),
                [
                    ROOM.li(data.sender),
                    ROOM.li(data.body)
                ]
            )
        );
    }

    static append = (destination, data) => {
        if (destination.querySelector('ul:last-of-type') != null) {
            if (destination.querySelector('ul:last-of-type').dataset.sender == data.sender) ROOM.appendLi(destination, data);
        }
        ROOM.appendUl(destination, data);
        ROOM.scroll();
    }

    static clear = () => {
        document.querySelector('#message').value = '';
    }

    static scroll = () => {
        ROOM.get().conversation.scrollTop = ROOM.get().conversation.scrollHeight;
    }
}