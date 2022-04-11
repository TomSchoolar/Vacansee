import api, { apiCatchError } from '@/assets/js/api';


describe('api error handler', () => {

    it('displays 400 error', () => {
        console.error = jest.fn();

        let error = {
            response: {
                data: {
                    'status': 400,
                    'message': 'bad request :('
                }
            }
        };

        apiCatchError(error);

        expect(console.error.mock.calls[0][0]).toBe('oops: 400: bad request :(');
    });

    it('ignores 401 error', () => {
        console.error = jest.fn();

        let error = {
            response: {
                data: {
                    'status': 401,
                    'message': 'unauthorised'
                }
            }
        };

        apiCatchError(error);

        expect(console.error.mock.calls.length).toBe(0);
    });

    it('displays unexpected errors', () => {
        console.error = jest.fn();

        let error = {
            toString: () => {
                return 'well this is a problem'
            }
        };

        apiCatchError(error);

        expect(console.error.mock.calls[0][0]).toBe('uh oh: well this is a problem');
    });

});