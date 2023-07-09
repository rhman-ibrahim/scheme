class Handler {
    static init = () => {
        Template.blurOff();
        Template.init();
        Aside.clear();
        Theme.init();
    }
    static copy = (element, attribute) => {
        let dataToCopy = element.getAttribute(`data-${attribute}`);
        navigator.clipboard.writeText(dataToCopy)
        .then(function() {
            alert("Link copied to clipboard!");
        })
        .catch(function() {
            alert("Failed to copy link to clipboard.");
        });
    }
}

class Template {
    static init = () => {
        document.documentElement.style.setProperty('--wh', `${window.innerHeight}px`);
        document.documentElement.style.setProperty('--ww', `${window.innerWidth}px`);
        if (Template.isThere('#space')) {
            const BOX = document.querySelector('#space-chat-box');
            BOX.style.width = `${BOX.parentElement.offsetWidth}px`;
        }
    }
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
}

class Aside {
    static close = selector => {
        document.querySelector(`${selector}`).addEventListener(
            'transitionend', () => {
                Template.blurOff();
            },
            {
                once: true
            }
        );
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

class Form {
    static passwordToggle = passwordToggleIcon => {
        document.querySelectorAll(`#${passwordToggleIcon.parentNode.parentNode.id} input.password`)
            .forEach(
                input => {
                    const type = input.getAttribute("type") === "password" ? "text" : "password";
                    input.setAttribute("type", type);
                }
            );
        grandChild.innerHTML = grandChild.innerHTML === "visibility" ? "visibility_off" : "visibility";
    }
}

class Theme {
    static init = () => {
        if (localStorage.getItem('theme') == null) Theme.default();
        else {
            document.body.classList.remove("dark", "light");
            document.body.classList.add(localStorage.getItem('theme'));
        }
        Theme.setIcon();
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
        if (Template.isThere('#theme')) {
            const icon = (localStorage.getItem("theme") == "dark") ? "dark_mode":"light_mode";
            document.querySelector('#theme').textContent = icon;
        }
    }
}

class Message {
    static close = button => {
        document.body.removeChild(button.parentNode.parentNode);
    }
}

class Thread {
    static init = () => {
        if (Template.isThere('.cards-s')) {
            let isDown = false;
            let startX, scrollLeft;
            document.querySelectorAll('.card-s').forEach(
                thread => {
                    thread.addEventListener('mousedown', (e) => {
                        isDown = true;
                        startX = e.pageX - thread.offsetLeft;
                        scrollLeft = thread.scrollLeft;
                    });
                    thread.addEventListener('mouseleave', () => {
                        isDown = false;
                    });
                    thread.addEventListener('mouseup', () => {
                        isDown = false;
                    });
                    thread.addEventListener('mousemove', (e) => {
                        if (!isDown) return;
                        e.preventDefault();
                        const x = e.pageX - thread.offsetLeft;
                        const walk = x - startX;
                        thread.scrollLeft = scrollLeft - walk;
                    });
                }
            );
        }
    }
    static next = item => {
        item.parentElement.scrollBy(
            {
                left: item.clientWidth,
                behavior: 'smooth'
            }
        );
    }
    static previous = item => {
        item.parentElement.scrollBy(
            {
                left: -item.clientWidth,
                behavior: 'smooth'
            }
        );
    }
    static first = item => {
        item.parentElement.scrollBy(
            {
                left: -(item.clientWidth * item.parentElement.childElementCount),
                behavior: 'smooth'
            }
        );
    }
    static last = item => {
        item.parentElement.scrollBy(
            {
                left: (item.clientWidth * item.parentElement.childElementCount),
                behavior: 'smooth'
            }
        );
    }
    static item = (selector, index) => {
        const thread = document.querySelector(`${selector}`);
        thread.querySelectorAll('.card').forEach(
            card => {
                card.style.outlineColor = "var(--d3)";
            }
        )
        thread.querySelector(`.card:nth-child(${index})`).style.outlineColor = "var(--di)";
        thread.querySelector(`.card:nth-child(${index})`)
        .scrollIntoView(
            {
                behavior: 'smooth'
            }
        );
    }
    static arrows = selector => {
        const i = "material-symbols-outlined";
        for (const card of document.querySelectorAll(`${selector}`)) {
            const f = document.createDocumentFragment();
            if (!card.nextElementSibling) {
                const first = document.createElement('i');
                first.setAttribute('class', i);
                first.setAttribute('onclick', 'Thread.first(this.parentElement)');
                first.textContent = "first_page";
                f.append(first);
            }
            if (card.previousElementSibling) {
                const previous = document.createElement('i');
                previous.setAttribute('class', i);
                previous.setAttribute('onclick', 'Thread.previous(this.parentElement)');
                previous.textContent = "keyboard_arrow_left";
                f.append(previous);
            }
            if (card.nextElementSibling) {
                const next = document.createElement('i');
                next.setAttribute('class', i);
                next.setAttribute('onclick', 'Thread.next(this.parentElement)');
                next.textContent = "keyboard_arrow_right";
                f.append(next);
            }
            card.appendChild(f);
        }
    }
}

class ConversationUI {
    static getSpace = () => {
        return document.querySelector('#space');
    }
    static messageUlElement = (destination, data) => {
        let ulElement          = document.createElement('ul');
        let mLiElement         = document.createElement('li');
        let uLiElement         = document.createElement('li');
        uLiElement.textContent = data.sender;
        mLiElement.textContent = data.body;
        ulElement.appendChild(uLiElement);
        ulElement.appendChild(mLiElement);
        ulElement.setAttribute('data-direction', (ConversationUI.getSpace().dataset.username == data.sender) ? 'out':'in');
        ulElement.setAttribute('data-sender', data.sender);
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