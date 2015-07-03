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

def post(data, *paths):
    uri = to_uri(*paths)
    response = session.post(uri, data=json.dumps(data))
    response.raise_for_status()
    return response.json()


print
print 'Selecting ads...'
ads = get('ads', offset=1, limit=5, approved='true')
ad_ids = [a['ad_id'] for a in ads]
print 'selected', ad_ids


print
print 'Creating retargeting campaign...'
to_retargeting_id = lambda a: 'clicks_{}'.format(ad['ad_id'])
# TODO: fill in your own campaign details
new_ad = {'url':'http://google.com',
          'name':'example ad name',
          'budget':1984,
          'bidmode':'Manual',
          'cpm_bid':3.1415,
          'creative_urls':['https://www.google.com.au/images/srpr/logo11w.png'],
          'start_date':datetime.datetime.now().isoformat(),
          'end_date':datetime.datetime.now().isoformat(),
          'blacklist':{'country':['Canada','France'],'site': ['tmz.com', 'dogecoin.com']}
          }
ad['targeting'] = {'device_groups':map(to_retargeting_id, ad_ids)} # NOTE: retargeting
print post(ad, 'ads')
