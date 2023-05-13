class Log {
    static list = () => {
        for (const log of document.querySelectorAll('.log')) log.style.display = "block";
    }
    static index = () => {
        Log.list();
    }
}

class Account {
    static history = account => {
        if (Template.isThere('.account.selected')) document.querySelector('.account.selected').classList.remove('selected');
        account.parentNode.parentNode.classList.add('selected');
        for (const log of document.querySelectorAll('.log')) {
            log.style.display = (log.dataset.accountId == Account.get()) ? "block":"none";
        }
        Slide.open('#left');
    }
    static set = account => {
        if (Template.isThere('.account.selected'))
        document.querySelector('.account.selected').classList.remove('selected');
        account.parentNode.parentNode.classList.add('selected');
        Slide.open('#control');
    }
    static get = () => {
        if (Template.isThere('.account.selected')) return document.querySelector('.account.selected').dataset.accountId;
        return false;
    }
    static toggleState = () => {
        if (Account.get()) {
            document.querySelector('#activation a').setAttribute('href',`/user/activation/${Account.get()}/`);
            Slide.open('#activation');
        }
    }
    static delete = () => {
        if (Account.get()) {
            document.querySelector('#deletion a').setAttribute('href',`/user/deletion/${Account.get()}/`);
            Slide.open('#deletion');
        }
    }
}