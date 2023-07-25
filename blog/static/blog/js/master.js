class Signal {
    static fields = () => {
        return {
            classification: document.getElementById('signal-classification-input'),
            icon: document.getElementById('signal-icon-input')
        }
    }
    static comment = () => {
        Signal.fields().classification.value = 1;
        Signal.fields().icon.value = "comment";
        Fixed.open('#signal-form-footer');
    }
    static criteria = () => {
        Signal.fields().classification.value = 2;
        Signal.fields().icon.value = "balance";
        Fixed.open('#signal-form-footer');
    }
    static decision = () => {
        Signal.fields().classification.value = 3;
        Signal.fields().icon.value = "gavel";
        Fixed.open('#signal-form-footer');
    }
    static hypothesis = () => {
        Signal.fields().classification.value = 4;
        Signal.fields().icon.value = "cognition";
        Fixed.open('#signal-form-footer');
    }
    static insight = () => {
        Signal.fields().classification.value = 5;
        Signal.fields().icon.value = "insights";
        Fixed.open('#signal-form-footer');
    }
    static metric = () => {
        Signal.fields().classification.value = 6;
        Signal.fields().icon.value = "monitoring";
        Fixed.open('#signal-form-footer');
    }
    static observation = () => {
        Signal.fields().classification.value = 7;
        Signal.fields().icon.value = "tips_and_updates";
        Fixed.open('#signal-form-footer');
    }
    static opportunity = () => {
        Signal.fields().classification.value = 8;
        Signal.fields().icon.value = "psychology";
        Fixed.open('#signal-form-footer');
    }
    static problem = () => {
        Signal.fields().classification.value = 9;
        Signal.fields().icon.value = "warning";
        Fixed.open('#signal-form-footer');
    }
    static question = () => {
        Signal.fields().classification.value = 10;
        Signal.fields().icon.value = "psychology_alt";
        Fixed.open('#signal-form-footer');
    }
    static default = () => {
        Signal.fields().classification.value = 11;
        Signal.fields().icon.value = "bubble_chart";
        Fixed.open('#signal-form-footer');
    }
    static test = () => {
        Signal.fields().classification.value = 12;
        Signal.fields().icon.value = "science";
        Fixed.open('#signal-form-footer');
    }
}