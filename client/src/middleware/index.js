const { logout } = require('@/assets/js/jwt');

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
        return logout();
    }

    session = JSON.parse(session);

    // flag gets deleted somehow
    if(typeof session.IsEmployer === 'undefined') {
        return logout();
    }

    if(session.IsEmployer === false) {
        router.push({ name: 'EmployeeIndex' });
    }

    return next();
}

middleware.isEmployee = ({ next, router }) => {
    let session = localStorage.getItem('session');

    if(!session) {
        return logout();
    }

    session = JSON.parse(session);

    // flag gets deleted somehow
    if (typeof session.IsEmployer === 'undefined') {
        return logout();        
    }

    if(session.IsEmployer === true) {
        router.push({ name: 'EmployerIndex' });
    }

    return next();
}

middleware.isNewEmployee = ({ next, router }) => {
    let session = localStorage.getItem('session');

    if(!session) {
        return logout();
    }

    session = JSON.parse(session);

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === true) {
        router.push({ name: 'EmployerIndex' });
    } else if(typeof session?.HasProfileSetup === 'undefined' || session.HasProfileSetup) {
        router.push({ name: 'EmployeeProfileEdit' });
    }

    return next();
    
}

middleware.hasProfile = ({ next, router }) => {
    let session = localStorage.getItem('session');

    if(!session) {
        return logout();
    }

    session = JSON.parse(session);

    if (typeof session.HasProfileSetup === 'undefined' || session.HasProfileSetup == false) {
        router.push({ name: 'EmployeeProfile' });
    }

    return next();
}


module.exports = middleware