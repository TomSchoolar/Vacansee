import axios from 'axios';
import createAuthRefreshInterceptor from 'axios-auth-refresh';

// create shared axios instance with some common defaults
let api = axios.create({
    baseURL: process.env.VUE_APP_API_ENDPOINT,
    timeout: 30000
    //timeout: 3000
});

// axios interceptor function that will be called to refresh authorisation if axios request fails with 401 status
const refreshAuthLogic = async (failedRequest) => {
    const tokenRefreshResponse = await api({
        url: '/refreshtoken/',
        method: 'post',
        skipAuthRefresh: true,
        responseType: 'json'
    }).catch(async (error) => {
        try {
            // error while refreshing access token
            let data = error.response.data;
            let { message = error?.message, status = 500 } = data;
            const refreshToken = localStorage.getItem('refreshToken');

            if(status == 401 || status == 403) {
                // authorisation error
                if(['login', 'register', 'forgot', 'reset'].includes(window.location.pathname.split('/')[1])) {
                    return false;
                }

                if(refreshToken != null) {
                    // refresh token available, can make logout request
                    await api({
                        url: '/logout/',
                        method: 'post',
                        skipAuthRefresh: true,
                    }).catch((err) => { console.error(err) })
                }

                window.localStorage.removeItem('accessToken');
                window.localStorage.removeItem('refreshToken');
                window.localStorage.removeItem('session');
                window.location.href = '/login'

            }

            console.error(`oops: ${ status }: ${ message }`);
        } catch {
            console.error(`uh oh: ${ error }`);
            alert('Error: Server may not be running');
        }
    });

    if(!tokenRefreshResponse?.data)
        return;

    localStorage.setItem('accessToken', tokenRefreshResponse.data.accessToken);
    localStorage.setItem('refreshToken', tokenRefreshResponse.data.refreshToken);
    failedRequest.response.config.headers['Authorization'] = `Bearer: ${ tokenRefreshResponse.data.accessToken }`;

    return Promise.resolve();
}

// instantiate the interceptor
createAuthRefreshInterceptor(api, refreshAuthLogic);

// custom interceptor to make sure that queued requests use the new access token
api.interceptors.request.use((request) => {
    // array contains urls of all routes that use refresh token instead of access token
    if(['/logout/', '/refreshtoken/'].includes(request.url)) {
        request.headers['Authorization'] = `Bearer: ${ localStorage.getItem('refreshToken') }`;
    } else {
        request.headers['Authorization'] = `Bearer: ${ localStorage.getItem('accessToken') }`;
    }
    return request;
});


// api request catch error handler
export const apiCatchError = (error) => {

    try {
        let data = error.response.data;
        let { message = error?.message, status = 500 } = data;

        if(status == 401) {
            // 401 errors will be handled by the refreshAuthLogic function
            return;
        }

        console.error(`oops: ${ status }: ${ message }`);
    } catch {
        console.error(`uh oh: ${ error }`);
        alert('Error: Server may not be running');
    }
}


export default api;
