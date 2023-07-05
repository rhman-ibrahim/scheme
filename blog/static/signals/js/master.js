class Signal {
    static update = signalNavOption => {
        let signal  = signalNavOption.parentNode.parentNode;
        let form    = document.querySelector(`#${signal.dataset.model}-create-form`);
        form.querySelector('[data-field=message]').value = "";
        form.setAttribute("action", `/signals/${signal.dataset.model}/update/${signal.dataset.id}/`);
        form.querySelector('[data-field=message]').value = signal.querySelector(".post-body li").textContent;
        form.querySelector('[data-field=parent]').value  = (isNaN(parseInt(signal.dataset.parent))) ? "":parseFloat(signal.dataset.parent);
        Slide.open(`#${signal.dataset.model}-create-form`);
    }
    static attach  = signalID => {
        document.querySelector(`#signal-create-form [data-field=parent]`).value  = signalID;
        document.querySelector('#signal-create-form [data-field=message]').value = "";
        Slide.open(`#signal-create-form`);
    }
    static comment  = signalNavOption => {
        let signal = signalNavOption.parentNode.parentNode;
        let form   = document.querySelector(`#comment-create-form`);
        form.querySelector('[data-field=message]').value = "";
        form.querySelector(`[data-field=post]`).value = signal.dataset.id;
        Slide.open(`#comment-create-form`);
    }
}