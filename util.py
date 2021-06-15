def pre_process_response(tweet: {}, includes: {}):
    ent = {}
    post = {'_id': tweet['id'], 'raw_text': tweet['text'], 'author_id': tweet['author_id']}
    retweeted = False
    for u in includes['users']:
        if u['id'] == post['author_id']:
            post['author_name'] = u['name']
            post['author_username'] = u['username']
            break
    post['created_at'] = tweet['created_at']
    if "possibly_sensitive" in tweet:
        post["possibly_sensitive"] = tweet["possibly_sensitive"]
    if 'referenced_tweets' in tweet:
        ref_tweets = []
        for rft in tweet['referenced_tweets']:
            ref_tweets.append({'id': rft['id'], 'type': rft['type']})
            if rft['type'] == 'retweeted':
                retweeted = True
                ref_id = rft['id']
                post['complete_text'] = False
                for p in includes['tweets']:
                    if p['id'] == ref_id:
                        post['raw_text'] = p['text']
                        post['complete_text'] = True
                        extract_context_annotation(post, p)
                        extract_entities(ent, p)
                        extract_mentions(ent, p)
                        break
        post["referenced_tweets"] = ref_tweets
    if not retweeted:
        extract_entities(ent, tweet)
        extract_context_annotation(post, tweet)

    extract_mentions(ent, tweet)
    post['twitter_entities'] = ent

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
    post['metrics'] = tweet['public_metrics']

    post['processed'] = False
    return post


def extract_context_annotation(post, tweet):
    if 'context_annotations' in tweet:
        post['twitter_context_annotations'] = tweet['context_annotations']


def extract_entities(ent, tweet):
    if 'entities' in tweet:
        if 'hashtags' in tweet['entities']:
            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['tag'])
            ent['hashtags'] = hashtags

        if 'urls' in tweet['entities']:
            urls = []
            for url in tweet['entities']['urls']:
                urls.append(url['url'])
            ent['urls'] = urls
        if 'annotations' in tweet['entities']:
            annotations = []
            for ann in tweet['entities']['annotations']:
                annotations.append(
                    {'type': ann['type'], 'normalized_text': ann['normalized_text'], 'probability': ann['probability']})
            ent['annotation'] = annotations


def extract_mentions(ent, tweet):
    if 'entities' in tweet:
        if 'mentions' in tweet['entities']:
            mentions = []
            for mention in tweet['entities']['mentions']:
                mentions.append(mention['username'])
            if 'mentions' in ent:
                ent['mentions'] += mentions
            else:
                ent['mentions'] = mentions
