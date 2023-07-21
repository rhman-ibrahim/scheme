class Circle {
    static loginForm = circleName => {
        document.querySelector('#circle-login-form #id_name').value = circleName;
        Fixed.open('#circle-login-form-footer');
    }
}