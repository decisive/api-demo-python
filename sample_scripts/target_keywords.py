import sys # NOTE: for exiting

import requests
import datetime
import pprint
import ujson as json # NOTE: faster json

API_KEY = '' # TODO: input api key here!!!
if not API_KEY:
    sys.exit('Please insert your Decisive API key')


print
print 'Creating session to always add API key...'
# NOTE: you can also use decisive.DecisiveApiClient
session = requests.Session()
session.auth = (API_KEY,'')

API_HOST = 'https://ads.decisive.is'
def to_uri(*paths, **get_args):
    path = '/'.join(p.strip('/') if isinstance(p,(str,unicode)) else unicode(p) for p in paths)
    args = '&'.join('{}={}'.format(*i) for i in get_args.items())
    return '{}/{}?{}'.format(API_HOST, path, args)

def get(*paths, **get_args):
    uri = to_uri(*paths, **get_args)
    response = session.get(uri)
    response.raise_for_status()
    return response.json()

def put(updated_ad):
    uri = to_uri('ads',updated_ad['ad_id'])
    response = session.put(uri, data=json.dumps(updated_ad))
    response.raise_for_status()
    return True


print
print 'Selecting ad...'
ads = get('ads', offset=1, limit=5, approved='true')
print [a['ad_id'] for a in ads]
ad = ads[0]
print 'selected', ad['ad_id']
pprint.pprint(ad['targeting'])


print
print 'Targeting keywords...'
ad['targeting']['keywords'] = ['game','test','music']
print put(ad)
