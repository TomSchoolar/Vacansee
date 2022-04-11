const middleware = {}

middleware.isLoggedIn = ({ next, router }) => {
    if(!localStorage.getItem('refreshToken') && !localStorage.getItem('accessToken')) {
        router.push({ name: 'LogIn' });
    }

    return next();
}

middleware.isNotLoggedIn = ({ next, router }) => {
    if(localStorage.getItem('refreshToken')) {
        // if logged in, redirect to respective home page
        const session = localStorage.getItem('session');

        if(!session) {
            window.localStorage.removeItem('accessToken');
            window.localStorage.removeItem('refreshToken');
        }

        if(session.IsEmployer)
            router.push({ name: 'EmployerIndex' });
        else
            router.push({ name: 'EmployeeIndex' });

        return next();
    }
    
    if(localStorage.getItem('accessToken')) {
        // not logged in but access token remains - corrupted
        localStorage.removeItem('accessToken');

    }
    
    if(localStorage.getItem('session')) {
        // not logged in but session remains - corrupted
        localStorage.removeItem('session');
    }

    return next();
}

middleware.isEmployer = ({ next, router }) => {
    let session = localStorage.getItem('session');

    if(!session) {
        router.push({ name: 'LogIn' });
    }

    session = JSON.parse(session);

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === false) {
        router.push({ name: 'EmployeeIndex' });
    }

    return next();
}

middleware.isEmployee = ({ next, router }) => {
    let session = localStorage.getItem('session');

    if(!session) {
        router.push({ name: 'LogIn' });
    }

    session = JSON.parse(session);

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === true) {
        router.push({ name: 'EmployerIndex' });
    }

    return next();
}


module.exports = middleware