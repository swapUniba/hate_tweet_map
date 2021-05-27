import http
import json
import time
import urllib

import geocoder
from tqdm import tqdm


def pre_process_response(tweet: {}, includes: {}):
    post = {'_id': tweet['id'], 'raw_text': tweet['text'], 'author_id': tweet['author_id']}
    for u in includes['users']:
        if u['id'] == post['author_id']:
            post['author_name'] = u['name']
            post['author_username'] = u['username']
            break
    post['created_at'] = tweet['created_at']
    if 'referenced_tweets' in tweet:
        for rft in tweet['referenced_tweets']:
            post['referenced_tweet'] = {'id': rft['id'], 'type': rft['type']}
            if rft['type'] == 'retweeted':
                for p in includes['tweets']:
                    if p['id'] == post['referenced_tweet']:
                        post['raw_text'] = p['text']
                        break

                break

    post['metrics'] = tweet['public_metrics']
    if 'entities' in tweet:
        ent = {}
        if 'hashtag' in tweet['entities']:
            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['tag'])
            ent['hashtags'] = hashtags

        if 'mentions' in tweet['entities']:
            mentions = []
            for mention in tweet['entities']['mentions']:
                mentions.append(mention['username'])
            ent['mentions'] = mentions

        if 'urls' in tweet['entities']:
            urls = []
            for url in tweet['entities']['urls']:
                urls.append(url['url'])
            ent['urls'] = urls

        post['twitter_entities'] = ent

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