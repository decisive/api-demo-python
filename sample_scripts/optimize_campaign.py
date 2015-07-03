import sys # NOTE: for exiting

import requests
import datetime
import pprint
import ujson as json # NOTE: faster json

API_KEY = '' # NOTE: input api key here!!!
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

def get_report(ad, type_, attribute, start_datehour, end_datehour, **options):
    return get('ads', ad['ad_id'], 'reports',
               type_, attribute,
               start_datehour.date().isoformat(),
               start_datehour.hour,
               end_datehour.date().isoformat(),
               end_datehour.hour,
               **options)

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
print 'Identify untargeted attributes...'
IGNORE_ATTRIBUTES = set(['city','creative_id','region','day_part','device_groups','os_version']) # NOTE: ignore attributes that are too specific
targeted_attributes = set(ad['targeting'].keys())
print targeted_attributes
available_attributes = set(get('audience','attributes')) - IGNORE_ATTRIBUTES
print available_attributes
untargeted_attributes = set(available_attributes) - set(targeted_attributes)
print untargeted_attributes


print
print 'Identifying segments with high spend potential...'
end_datehour = datetime.datetime.now()
start_datehour = end_datehour - datetime.timedelta(days=7)
select_segment = lambda r: 'unknown' not in r[attribute].lower() and r['bids'] > 10
for attribute in untargeted_attributes:
    report = get_report(ad, 'aggregate', attribute, 
                        start_datehour, end_datehour,
                        select='bids',
                        sort='spend',
                        limit=5)
    pprint.pprint(report); print
    if report:
        ad['targeting'][attribute] = [r[attribute] for r in report if select_segment(r)]
print 'Optimized targeting'
pprint.pprint(ad['targeting'])


print
print 'Identifying segments with low conversion rate...'
for attribute in targeted_attributes:
    report = get_report(ad, 'aggregate', attribute, 
                        start_datehour, end_datehour,
                        select='bids',
                        sort='cvr', # NOTE: converation rate
                        limit=5,
                        ascending='true')
    pprint.pprint(report); print
    if report:
        ad['blacklist'][attribute] = [r[attribute] for r in report if select_segment(r)]
print 'Optimized blacklist'
pprint.pprint(ad['blacklist'])


print
print 'Updating ad...'
print put(ad)
