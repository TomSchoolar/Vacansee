const middleware = {}

middleware.isLoggedIn = ({ next, router }) => {
    if(!localStorage.getItem('session') || !localStorage.getItem('accessToken') || !localStorage.getItem('refreshToken')) {
        return router.push({ name: 'LogIn' });
    }

    return next();
}

middleware.isNotLoggedIn = ({ next, router }) => {
    if(localStorage.getItem('accessToken') && localStorage.getItem('session') && localStorage.getItem('refreshToken')) {
        // if logged in, redirect to respective home page
        const { IsEmployer = false } = localStorage.getItem('session');
        if(IsEmployer)
            return router.push({ name: 'EmployerIndex' });
        return router.push({ name: 'EmployeeIndex' });

    }
    
    if(localStorage.getItem('accessToken')) {
        // not logged in but jwt remains - corrupted
        localStorage.removeItem('accessToken');

    }
    
    if(localStorage.getItem('session')) {
        // not logged in but session remains - corrupted
        localStorage.removeItem('session');
    }

    if(localStorage.getItem('refreshToken')) {
        // not logged in but refresh token remains - corrupted
        localStorage.removeItem('refreshToken')
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