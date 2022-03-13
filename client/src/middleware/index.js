const middleware = {}

middleware.isLoggedIn = ({ next, router }) => {
    if(!localStorage.getItem('jwt') || !localStorage.getItem('session')) {
        return router.push({ name: 'LogIn' });
    }

    return next();
}

middleware.isEmployer = ({ next, router }) => {
    const session = JSON.parse(localStorage.getItem('session'));
    console.log(session)
    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === false) {
        return router.push({ name: 'EmployeeIndex' });
    }

    return next();
}

middleware.isEmployee = ({ next, router }) => {
    const session = JSON.parse(localStorage.getItem('session'));
    console.log(session)
    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === true) {
        return router.push({ name: 'EmployerIndex' });
    }

    return next();
}


module.exports = middleware