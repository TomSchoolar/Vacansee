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
        const { IsEmployer = false } = localStorage.getItem('session');
        if(IsEmployer)
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
    const session = JSON.parse(localStorage.getItem('session'));

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === false) {
        router.push({ name: 'EmployeeIndex' });
    }

    return next();
}

middleware.isEmployee = ({ next, router }) => {
    const session = JSON.parse(localStorage.getItem('session'));

    if(typeof session.IsEmployer === 'undefined' || session.IsEmployer === true) {
        router.push({ name: 'EmployerIndex' });
    }

    return next();
}


module.exports = middleware