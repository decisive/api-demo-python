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

def post(data, *paths):
    uri = to_uri(*paths)
    response = session.post(uri, data=json.dumps(data))
    response.raise_for_status()
    return response.json()


print
print 'Creating ad...'
# TODO: fill in your own campaign details
ad = {'url':'http://google.com',
      'name':'example ad name',
      'budget':1984,
      'bidmode':'Manual',
      'cpm_bid':3.1415,
      'creative_urls':['https://www.google.com.au/images/srpr/logo11w.png'],
      'start_date':datetime.datetime.now().isoformat(),
      'end_date':datetime.datetime.now().isoformat(),
      'blacklist':{'country':['Canada','France'],'site': ['tmz.com', 'dogecoin.com']},
      'targeting':{'country':['Mexico']}
      }
new_creative_urls = ['https://www.google.com.au/logos/2014/halloween14/5.gif']
sys.exit('TODO: remove once finished testing')
ad_id = post(ad, 'ads')['ad_id']
print ad_id
print post(new_creative_urls, 'ads',ad_id,'creatives')
print get('ads',ad_id)