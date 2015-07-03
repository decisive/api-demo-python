import requests
import requests.exceptions

import datetime
import ujson as json

import logging

class DecisiveApiClient(object):
    HOST = 'https://ads.decisive.is'.strip('/')
    
    def __init__(self, api_key, host=None):
        self.session = requests.Session()
        self.session.auth = (api_key,'')
        self.host = host or DecisiveApiClient.HOST

    def to_uri(self, *paths, **get_args):
        path = '/'.join(p.strip('/') for p in map(unicode, paths))
        args = '&'.join('{}={}'.format(*i) for i in get_args.items())
        return '{}/{}?{}'.format(self.host, path, args)

    def get(self, *paths, **get_args):
        uri = self.to_uri(*paths, **get_args)
        response = self.session.get(uri)
        return self.examine_response(response)

    def put(self, updated_ad): # NOTE: only /ads supports PUT method at the moment
        uri = self.to_uri('ads',updated_ad['ad_id'])
        response = self.session.put(uri, data=json.dumps(updated_ad))
        return self.examine_response(response, False)

    def post(data, *paths):
        uri = self.to_uri(*paths)
        response = self.session.post(uri, data=json.dumps(data))
        return self.examine_response(response)
    
    def delete(*paths):
        uri = self.to_uri(*paths)
        response = self.session.delete(uri)
        return self.examine_response(response, False)
    
    def get_report(self, ad, type_, attribute, start_datehour, end_datehour, **options):
        return self.get('ads', ad['ad_id'], 'reports',
                        type_, attribute,
                        start_datehour.date().isoformat(),
                        start_datehour.hour,
                        end_datehour.date().isoformat(),
                        end_datehour.hour,
                        **options)
    
    def examine_response(response, return_json=True):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            body = (response.json() or {})
            message = body.get('reason') or error.messsage
            logging.warning('HTTPError', response.status_code, message)
            logging.info('Did you know?', body.get('did_you_know'))
            return False
        return True if not return_json else response.json()

