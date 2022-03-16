const middleware = {}

middleware.isLoggedIn = ({ next, router }) => {
    if(!localStorage.getItem('jwt') || !localStorage.getItem('session')) {
        return router.push({ name: 'LogIn' });
    }

    return next();
}

middleware.isNotLoggedIn = ({ next, router }) => {
    if(localStorage.getItem('jwt') && localStorage.getItem('session')) {
        // if logged in, redirect to respective home page
        const { IsEmployer = false } = localStorage.getItem('session');
        if(IsEmployer)
            return router.push({ name: 'EmployerIndex' });
        return router.push({ name: 'EmployeeIndex' });

    } else if(localStorage.getItem('jwt')) {
        // not logged in but jwt remains - corrupted
        localStorage.removeItem('jwt');

    } else if(localStorage.getItem('session')) {
        // not logged in but session remains - corrupted
        localStorage.removeItem('session');
    }

    return next();
}

middleware.isEmployer = ({ next, router }) => {
    const session = JSON.parse(localStorage.getItem('session'));

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === false) {
        return router.push({ name: 'EmployeeIndex' });
    }

    return next();
}

middleware.isEmployee = ({ next, router }) => {
    const session = JSON.parse(localStorage.getItem('session'));

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === true) {
        return router.push({ name: 'EmployerIndex' });
    }

    return next();
}


module.exports = middleware