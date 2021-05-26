import http
import json
import time
import urllib

import geocoder
from tqdm import tqdm


def pre_process_response(tweet: {}, includes: {}):
    post = {'_id': tweet['id'], 'author_id': tweet['author_id'], 'raw_text': tweet['text']}
    if 'referenced_tweets' in tweet:
        for rft in tweet['referenced_tweets']:
            if rft['type'] == 'retweeted':
                post['referenced_tweet'] = rft['id']
                for p in includes['tweets']:
                    if p['id'] == post['referenced_tweet']:
                        post['raw_text'] = p['text']
                        break
                break

    post['metrics'] = tweet['public_metrics']
    if 'entities' in tweet:
        if 'hashtag' in tweet['entities']:
            hashtags = ""
            for hashtag in tweet['entities']['hashtags']:
                hashtags += " " + hashtag['tag']
            post['hashtags'] = hashtags

        if 'mentions' in tweet['entities']:
            mentions = ""
            for mention in tweet['entities']['mentions']:
                mentions += " " + mention['username']
            post['mentions'] = mentions

        if 'urls' in tweet['entities']:
            urls = ""
            for url in tweet['entities']['urls']:
                urls += " " + url['url']
            post['urls'] = urls

    if 'context_annotations' in tweet:
        post['twitter_context_annotations'] = tweet['context_annotations']
    if 'geo' in tweet:
        post['geo_id'] = tweet['geo']['place_id']
        for p in includes['places']:
            if p['id'] == post['geo_id']:
                post['country'] = p['country']
                post['city'] = p['full_name']
                # latitude, longitude = get_osm_coordinates(post['city'] + "," + post['country'])
                # latitude, longitude = get_openstack_coordinates(post['city'] ,post['country'])

                # post["coordinates"] = str(latitude) + "," + str(longitude)
                break
    post['processed'] = False
    return post





def get_openstack_coordinates(query, region):
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': 'e312d9e11a7a630e41d196cdde9ba5dd',
        'query': query,
        'region': region,
        'limit': 1,
        'output': 'json'
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    json_r = json.loads(data)

    if json_r:
        if 'data' in json_r:
            d = json_r['data']
            if len(d) > 0:
                if len(d[0]) > 0:
                    return d[0]['latitude'], d[0]['longitude']
    return "",""