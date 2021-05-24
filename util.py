import geocoder


def pre_process_response(twitter_results: []):
    tweets_processed = []
    for tweets in twitter_results:
        for t in tweets['data']:
            post = {'_id': t['id'], 'author_id': t['id'], 'raw_text': t['text']}
            if 'referenced_tweets' in t:
                for rft in t['referenced_tweets']:
                    if rft['type'] == 'retweeted':
                        post['referenced_tweet'] = rft['id']
                        for p in tweets['includes']['tweets']:
                            if p['id'] == post['referenced_tweet']:
                                post['raw_text'] = p['text']
                                break
                        break

            post['metrics'] = t['public_metrics']
            if 'entities' in t:
                if 'hashtag' in t['entities']:
                    hashtags = ""
                    for hashtag in t['entities']['hashtags']:
                        hashtags += " " + hashtag['tag']
                    post['hashtags'] = hashtags

                if 'mentions' in t['entities']:
                    mentions = ""
                    for mention in t['entities']['mentions']:
                        mentions += " " + mention['username']
                    post['mentions'] = mentions

                if 'urls' in t['entities']:
                    urls = ""
                    for url in t['entities']['urls']:
                        urls += " " + url['url']
                    post['urls'] = urls

            if 'context_annotations' in t:
                post['twitter_context_annotations'] = t['context_annotations']
            if 'geo' in t:
                post['geo_id'] = t['geo']['place_id']
                for p in tweets['includes']['places']:
                    if p['id'] == post['geo_id']:
                        post['country'] = p['country']
                        post['city'] = p['full_name']
                        latitude, longitude = get_coordinates(post['city'] + "," + post['country'])
                        post["coordinates"] = str(latitude) + "," + str(longitude)
                        break
            post['processed'] = str(False)
            tweets_processed.append(post)
    return tweets_processed


def get_coordinates(address: ""):
    g = geocoder.osm(address)
    return g.osm['y'], g.osm['x']
