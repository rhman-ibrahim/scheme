
class ROOM {
    
    static get = () => {
        return {
            ui: document.querySelector('#messages'),
            last: document.getElementById('messages').querySelector('ul:last-of-type'),
            username: String(document.getElementById('user-username').value),
            message: String(document.getElementById('room-message').value),
            identifier: String(document.getElementById('room-identifier').value),
            token: String(document.getElementById('user-token').value)
        };
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
            if (destination.querySelector('ul:last-of-type').dataset.sender == data.sender) {
                ROOM.appendLi(destination, data);
            }
        }
        ROOM.appendUl(destination, data);
        ROOM.scroll();
    }

    static scroll = () => ROOM.get().ui.scrollTop = ROOM.get().ui.scrollHeight;
    static input  = () => ROOM.get().message.trim().length !== 0 ? true:false;
    static clear  = () => document.getElementById('room-message').value = '';
}