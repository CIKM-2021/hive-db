import falcon

from ..conf import settings


class APIPermission:
    '''
        This will handle all incoming requests.
        Incoming requests should include a header:
        Token - [secret key]
    '''

    def process_request(self, req, resp):
        token = req.headers.get('TOKEN', None)

        if token != settings.HIVE_KEY:
            raise falcon.HTTPUnauthorized()
