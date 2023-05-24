class Handler {
    static init = () => {
        Template.init();
        Theme.default();
        Form.init();
        Thread.init();
    }
}

class Template {
    static init = () => {
        document.documentElement.style.setProperty('--wh', `${window.innerHeight}px`);
        document.documentElement.style.setProperty('--ww', `${window.innerWidth}px`);
    }
    static isThere = selector => {
        if (document.body.contains(document.querySelector(`${selector}`))) return true;
        return false;
    }
    static isVisible = element => {
        if (window.getComputedStyle(element).display === 'block') return element;
    }
    static blur = (state, selector) => {
        const elem = document.querySelector(`${selector}`);
        const main = document.querySelector('main');
        if (state == true) {
            if (main.contains(elem)) {
                document.querySelectorAll('aside:not(.active)').forEach(
                    column => {
                        column.style.filter = "blur(5px)";
                    }
                );
            } else {
                document.querySelector('main').style.filter = "blur(5px)";
            }
        } else {
            if (main.contains(elem)) {
                document.querySelectorAll('aside').forEach(
                    column => {
                        column.style.filter = "none";
                    }
                );
            } else {
                document.querySelector('main').style.filter = "none";
            }
        }
    }
}

class Aside {
    static open = selector => {
        Aside.clear();
        document.querySelector(`${selector}`).classList.add('active');
        localStorage.setItem('aside', selector);
        Template.blur(true, selector);
    }
    static close = selector => {
        document.querySelector(`${selector}`).classList.remove('active');
        localStorage.removeItem('aside');
        Template.blur(false, selector);
    }
    static clear = () => {
        let aside = localStorage.getItem('aside');
        if (aside !== null && Template.isThere(`${localStorage.getItem('aside')}`)) {
            Aside.close(aside);
        }
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
    static init = () => {
        if (Form.collect().length > 0) Form.correctHeights();
    }
    static collect = () => {
        return document.querySelectorAll('form').length;
    }
    static correctHeights = () => {
        for (const form in document.querySelectorAll('form')) {
            form.style.height = `-${form.offsetHeight * 2}px`;
        }
    }
    static passwordToggle = grandChild => {
        document.querySelectorAll(`#${grandChild.parentNode.parentNode.parentNode.id} input.password`)
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
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener(
            'change', (e) => {
                if (e.matches) Theme.dark();
                else Theme.light();
            }
        );
    }
    static default = () => {
        document.body.classList.remove("dark", "light");
        let theme = (window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark":"light";
        localStorage.setItem("theme", theme);
        document.body.classList.add(theme);
        Theme.setIcon();
        Theme.init();
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
        document.body.removeChild(button.parentNode);
    }
}

class Thread {
    static init = () => {
        if (Template.isThere('.cards-h')) {
            let isDown = false;
            let startX, scrollLeft;
            document.querySelectorAll('.card-h').forEach(
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