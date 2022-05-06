import api, { apiCatchError } from '@/assets/js/api';


export const logout = async () => {
    // send logout request to api and on success, remove tokens from storage

    const response = await api({
        url: '/v1/logout/',
        method: 'post'
    }).catch(apiCatchError);

    if(response) {
        window.localStorage.removeItem('accessToken');
        window.localStorage.removeItem('refreshToken');
        window.localStorage.removeItem('session');
        window.location.href = '/login'
    }
}
