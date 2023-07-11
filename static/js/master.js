class Grid {
    static init = () => {
        Grid.setDimensions();
        Grid.fixChatBoxWidth();
        Grid.justifyColumnContent();
    }
    static setDimensions = () => {
        document.documentElement.style.setProperty('--wh', `${window.innerHeight}px`);
        document.documentElement.style.setProperty('--ww', `${window.innerWidth}px`);
    }
    static fixChatBoxWidth = () => {
        if (Template.isThere('#space')) {
            const BOX = document.querySelector('#space-chat-box');
            BOX.style.width = `${BOX.parentElement.offsetWidth}px`;
        }
    }
    static justifyColumnContent = () => {
        document.querySelectorAll('#left, #right')
        .forEach(
            column => {
                let widgetsTotalHeights = 0;
                column.querySelectorAll('.widget, .aside-nav')
                .forEach(
                    widget => widgetsTotalHeights += widget.clientHeight);
                if ((widgetsTotalHeights / window.innerHeight) < .75) {
                    column.style.justifyContent = "center";
                }    
            }
        );
    }
}


class Aside {
    static init = () => {
        let asideSelector = String(localStorage.getItem('aside'));
        if (asideSelector.includes('form')) Aside.open(asideSelector); else Aside.clear();
    }
    static close = selector => {
        Template.blurOff();
        document.querySelector(`${selector}`).classList.remove('active');
        localStorage.removeItem('aside');
    }
    static clear = () => {
        let aside = localStorage.getItem('aside');
        if (aside !== null && Template.isThere(`${localStorage.getItem('aside')}`)) {
            Aside.close(aside);
        }
    }
    static open = selector => {
        Aside.clear();
        Template.blurOn(selector);
        document.querySelector(`${selector}`).classList.add('active');
        localStorage.setItem('aside', selector);
    }
    static toggle = selector => {
        if (selector == localStorage.getItem('aside')) {
            (Template.isThere(selector)) ? Aside.close(selector) : Aside.open(selector);
        } else {
            Aside.open(selector);
        }
    }
}


class Template {
    static isThere = selector => {
        if (document.body.contains(document.querySelector(`${selector}`))) return true;
        return false;
    }
    static isVisible = element => {
        if (window.getComputedStyle(element).display === 'block') return element;
    }
    static blurOff = () => {
        document.querySelectorAll('main > *').forEach(
            column => {
                column.style.filter = "none";
            }
        );
    }
    static blurOn = selector => {
        document.querySelectorAll('main > *').forEach(
            column => {
                column.style.filter = "blur(5px)";
            }
        );
        document.querySelector(`${selector}`).style.filter = "none";
    }
    static writeToClipboard = (element, attribute) => {
        let dataToCopy = element.getAttribute(`data-${attribute}`);
        navigator.clipboard.writeText(dataToCopy)
        .then(
            () => alert("Link copied to clipboard!"))
        .catch(
            () => alert("Failed to copy link to clipboard.")
        )
    }
}


class Form {
    static passwordToggle = passwordToggleButton => {
        document.querySelectorAll(`#${passwordToggleButton.parentNode.parentNode.id} input.password`)
        .forEach(
            input => {
                const type = input.getAttribute("type") === "password" ? "text" : "password";
                input.setAttribute("type", type);
            }
        );
    }
}


class Message {
    static list = () => {
        const messagesIdSelectors = []; 
        document.querySelectorAll('.message').forEach(message => messagesIdSelectors.push(message.id));
        return messagesIdSelectors;
    }
    static init = () => {
        if (Message.list().length) Aside.open(`#${Message.list()[0]}`);
    }
    static next = selector => {
        Aside.close(`#${selector}`);
        const list      = Message.list();
        const index     = list.indexOf(selector);
        const nextIndex = index + 1;
        list.splice(index, 1);
        if (list.length >= nextIndex) Aside.open(`#${Message.list()[nextIndex]}`);
    }
}


class ConversationUI {
    static messageUlElement = (destination, data) => {
        let ulElement          = document.createElement('ul');
        let mLiElement         = document.createElement('li');
        let uLiElement         = document.createElement('li');
        uLiElement.textContent = data.sender;
        mLiElement.textContent = data.body;
        ulElement.appendChild(uLiElement);
        ulElement.appendChild(mLiElement);
        ulElement.setAttribute(
            'data-direction', (document.querySelector('#space').dataset.username == data.sender) ? 'out':'in'
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
            ConversationUI.messageLiElement(destination, data);
        } else {
            ConversationUI.messageUlElement(destination, data);
        }
        ConversationUI.scrollToDestination(destination);
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

class Theme {
    static init = () => {
        if (localStorage.getItem('theme') == null) Theme.default();
        else {
            document.body.classList.remove("dark", "light");
            document.body.classList.add(localStorage.getItem('theme'));
        }
    }
    static default = () => {
        document.body.classList.remove("dark", "light");
        let theme = (window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark":"light";
        localStorage.setItem("theme", theme);
        document.body.classList.add(theme);
        Theme.setIcon();
    }
    static dark = () => {
        document.body.classList.remove(localStorage.getItem('theme'));
        localStorage.setItem("theme", "dark");
        document.body.classList.add(localStorage.getItem('theme'), "dark");
        Theme.setIcon();
    }
    static light = () => {
        document.body.classList.remove(localStorage.getItem('theme'));
        localStorage.setItem("theme", "light");
        document.body.classList.add(localStorage.getItem('theme'), "light");
        Theme.setIcon();
    }
    static toggle = () => {
        document.body.classList.remove(localStorage.getItem('theme'));
        localStorage.setItem("theme", (localStorage.getItem("theme") == "dark") ? "light" : "dark");
        document.body.classList.add(localStorage.getItem('theme'));
        Theme.setIcon();
    }
    static setIcon = () => {
        if (Template.isThere('#theme-icon')) {
            const icon = (localStorage.getItem("theme") == "dark") ? "dark_mode":"light_mode";
            document.querySelector('#theme-icon').textContent = icon;
        }
    }
}


class Handler {
    static init = () => {
        Grid.init();
        Aside.init();
        Theme.init();
        Message.init();
    }
}