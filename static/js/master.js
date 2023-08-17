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
    static setIcon = () => {
        if (Template.isThere('#theme-icon')) {
            const icon = (localStorage.getItem("theme") == "dark") ? "dark_mode":"light_mode";
            document.querySelector('#theme-icon').textContent = icon;
        }
    }
}


class Grid {
    static init = () => {
        Grid.setDimensions();
        Grid.justifyColumnContent();
    }
    static setDimensions = () => {
        document.documentElement.style.setProperty('--wh', `${window.innerHeight}px`);
        document.documentElement.style.setProperty('--ww', `${window.innerWidth}px`);
    }
    static justifyColumnContent = () => {
        document.querySelectorAll('section:not(#main) div.column')
        .forEach(
            column => {
                let widgetsTotalHeights = 0;
                column.querySelectorAll('.widget').forEach(
                    widget => widgetsTotalHeights += widget.clientHeight
                );
                if ((widgetsTotalHeights / window.innerHeight) < .75) {
                    column.style.justifyContent = "center";
                }
            }
        );
    }
}

class Blurred {
    static append = () => {
        return new Promise(
            resolve => {
                if (!Template.isThere('#blurred-layer')) {
                    const blurredLayer = document.createElement('div');
                    blurredLayer.setAttribute('onclick', 'Blurred.check()');
                    blurredLayer.setAttribute('id', 'blurred-layer');
                    document.body.appendChild(blurredLayer);
                }
                resolve();       
            }
        )
    }
    static check = () => {
        if (Fixed.collected() != null) {
            if (Fixed.collected().classList.contains('message')) {
                Message.next(Fixed.collected().id);
                if (Message.list().length == 0) Fixed.clear();
            } else {
                Fixed.clear();
            }
        } else {
            Fixed.clear();
        }
    }
    static remove = () => {
        return new Promise(
            resolve => {
                Template.remove('#blurred-layer');
                resolve();
            }
        )
    }
}

class Fixed {
    static collected = () => {
         return localStorage.getItem('fixed') ? document.querySelector(localStorage.getItem('fixed')) : null;
    }
    static close = selector => {
        Blurred.remove()
        .then(
            () => {
                if (Template.isThere(selector)) {
                    document.querySelector(selector).classList.remove('active');
                }
                localStorage.removeItem('fixed');
            }
        )
    }
    static clear = () => {
        Fixed.close(localStorage.getItem('fixed'));
    }
    static open = selector => {
        Fixed.clear();
        Blurred.append()
        .then(
            () => {
                if (Template.isThere(selector)) {
                    document.querySelector(`${selector}`).classList.add('active');
                    localStorage.setItem('fixed', selector);
                }
            }
        )
    }
    static CircleLoginForm = circleName => {
        document.querySelector('#circle-login-form #id_name').value = circleName;
        Fixed.open('#circle-login-form');
    }
    static init = () => {
        if (Fixed.collected()) Fixed.open(localStorage.getItem('fixed')); else localStorage.removeItem('fixed');         
    }
    static toggle = selector => {
        localStorage.getItem('fixed') == selector ? Fixed.close(selector) : Fixed.open(selector);
    }
}


class Message {
    static list = () => {
        const messagesIdSelectors = []; 
        document.querySelectorAll('.message').forEach(message => messagesIdSelectors.push(message.id));
        return messagesIdSelectors;
    }
    static init = () => {
        if (Message.list().length) Fixed.open(`#${Message.list()[0]}`);
    }
    static next = selector => {
        Template.remove(`#${selector}`);
        const list      = Message.list();
        const index     = list.indexOf(selector);
        const nextIndex = index + 1;
        if (list.length >= nextIndex) Fixed.open(`#${Message.list()[nextIndex]}`);
    }
    static index = selector => {
        const list = Message.list();
        return (list.indexOf(selector) / list.length)
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


class Template {
    static isThere = selector => {
        if (document.body.contains(document.querySelector(`${selector}`))) return true;
        return false;
    }
    static isVisible = element => {
        if (window.getComputedStyle(element).display === 'block') return element;
    }
    static remove = selector => {
        let element = document.querySelector(selector);
        if (document.body.contains(element)) document.body.removeChild(element);
    }
    static append = (parent, children) => {
        children.forEach(child => parent.appendChild(child));
        return parent;
    }
    static copyToClipboard = element => {
        let dataToCopy = element.getAttribute(`data-clipboard`);
        navigator.clipboard.writeText(dataToCopy)
        .then(
            () => alert("copied to clipboard!"))
        .catch(
            () => alert("Failed to copy to clipboard.")
        )
    }
}

class Timer {
    static countDown = () => {
        let x = new Date(document.getElementById("timer").dataset.countDown);
        x.setUTCHours(x.getUTCHours() + 3);
        x = x.getTime();
        setInterval(
            () =>
            {
                let dif = x - new Date().getTime();
                console.log(dif);
                    
                // Time calculations for days, hours, minutes and seconds
                let h = Math.floor((dif % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let m = Math.floor((dif % (1000 * 60 * 60)) / (1000 * 60));
                let s = Math.floor((dif % (1000 * 60)) / 1000);

                document.getElementById("timer").innerHTML = `${h}:${m}:${s}`;
                    
                // If the count down is over, write some text 
                if (dif < 0) {
                    clearInterval(x);
                    window.location.href = `http://${window.location.host}/user/deactivate`
                }
            },
            1000
        );
    }
}

class Handler {
    static init = () => {
        Grid.init();
        Theme.init();
        Message.init();
        if (Template.isThere('#timer')) Timer.countDown();
    }
}