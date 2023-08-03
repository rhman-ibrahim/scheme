class Signal {

    static fields = () => {
        return {
            classification: document.getElementById('signal-classification-input'),
            glyph: document.getElementById('signal-glyph-input'),
            icon: document.getElementById('signal-icon-input'),
            body: document.getElementById('id_body')
        }
    }

    static get = iElement => {
        return {
            placeholder: iElement.parentElement.parentElement.querySelector('p').textContent,
            classification: iElement.parentElement.parentElement.querySelector('h4 b').textContent,
            glyph: iElement.classList.item(0),
            icon: iElement.textContent
        }
    }
    
    static set = iElement => {
        return new Promise(
            resolve => {
                const signal = Signal.get(iElement);
                Signal.fields().classification.setAttribute('value', signal.classification);
                Signal.fields().body.setAttribute('placeholder',signal.placeholder);
                Signal.fields().glyph.setAttribute('value', signal.glyph);
                Signal.fields().icon.setAttribute('value', signal.icon);
                resolve();
            }
        )
    }

    static form = (iElement) => {
        Signal.set(iElement).then(Fixed.open('#signal-form-footer'));
    }

}