import axios from 'axios';

const functions = {};


export const getAccessToken = () => {
    // return accessToken from local storage
    let token = window.localStorage.getItem('accessToken');
    if(token)
        return token;
    return false;
}


export const getRefreshToken = () => {
    // return refreshToken from local storage
    let token = window.localStorage.getItem('refreshToken');
    if(token)
        return token;
    return false;
}


export const parseToken = () => {
    // return json version of jwt
    let token = functions.getAccessToken();

    if(!token)
        return false;

    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};


export const getIdFromToken = () => {
    // return uid from jwt
    let token = functions.getAccessToken();
    if(!token)
        return false;

    jwt = functions.parseToken(token)
    return jwt.id;
}


export const logout = async () => {
    // send logout request to api and on success, remove tokens from storage

    const refreshToken = getRefreshToken();

    const response = await axios({
        url: '/logout/',
        baseURL: process.env.VUE_APP_API_ENDPOINT,
        method: 'post',
        timeout: 3000,
        headers: {
            authorization: `Bearer: ${ refreshToken }`
        }
    }).catch((err) => {
        console.error(`uh oh: ${ err }`);
        alert('An error was encountered while logging you out')
        return false;
    });

    if(response) {
        window.localStorage.removeItem('accessToken');
        window.localStorage.removeItem('refreshToken');
        window.localStorage.removeItem('session');
        window.location.href = '/login'
    }
}