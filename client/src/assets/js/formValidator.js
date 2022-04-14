export default (schema, data, options = {}) => {
    const { addErrorToParent = false } = options;

    // clear validation error styles
    document.querySelectorAll('.invalid-input').forEach((el) => el.classList.remove('invalid-input'));
    document.querySelectorAll('.validation-error-message-label').forEach((el) => el.remove());

    // validate form and handle any errors
    const { error, value } = schema.validate(data);

    try {
        if(error) {
            const details = error.details;
            const erroneousInput = document.querySelector(`*[name='${ details[0]?.path[0] }']`);
            erroneousInput.classList.add('invalid-input');

            if(addErrorToParent && addErrorToParent.includes(details[0]?.path[0]))
                erroneousInput.parentElement.insertAdjacentElement('afterend', createErrorMessage(details));
            else
                erroneousInput.insertAdjacentElement('afterend', createErrorMessage(details));
            return false;
        }
        return true;
    } catch(err) {
        alert('invalid inputs');
        console.error(err);
    }
}


const createErrorMessage = (details) => {
    const div = document.createElement('div');
    div.classList.add('validation-error-message-label');
    div.style.cssText = `
        color: var(--red);
        font-size: 11px;
        margin: 0;
        font-weight: bold;
        display: flex;
        justify-content: flex-start;
        text-align: left;
    `;
    div.innerText = details[0].message;
    return div;
}