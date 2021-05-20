import string
import it_core_news_lg
import requests
import json
import time
from spacy.pipeline.ner import DEFAULT_NER_MODEL

import spacy
from pymongo import MongoClient
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
# import tagme
import MyTagMe

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAPtPgEAAAAAoVlZ4I0szkcu4dL%2Bhqif%2F%2BF45Oo%3DJbvSo773bskLu1GexDv9Dq1HjuSjfSwfxgLdDXEdlPO5mKyE6G'

search_url = "https://api.twitter.com/2/tweets/search/all"


def next_page(next_token="", query={}):
    if next_token != "":
        query["next_token"] = next_token
    return query


def make_query(keywords="", language="it", place="italia", place_country='IT', user=""):
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query = {}

    if keywords == "" and user == "":
        return ""
    else:
        if keywords != "":
            query['query'] = keywords
        if user != "":
            query['from'] = user
        query['query'] += " lang:" + language
        # query['place'] = place
        query['query'] += " place_country:" + place_country
        query['place.fields'] = "contained_within,country,country_code,full_name,geo,id,name,place_type"
        query['expansions'] = 'geo.place_id'
        query['tweet.fields'] = 'author_id' + ',public_metrics,context_annotations,entities'

    return query


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(bearer_token)
    q = make_query("#palestina")
    json_response = connect_to_endpoint(search_url, headers, q)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    time.sleep(2)
    save_on_db(json_response)
    remake(json_response, q)


def remake(response, query):
    if "meta" in response:
        if "next_token" in response['meta']:
            headers = create_headers(bearer_token)
            json_response = connect_to_endpoint(search_url, headers,
                                                next_page(next_token=response["meta"]["next_token"], query=query))
            print(json.dumps(json_response, indent=4, sort_keys=True))
            time.sleep(2)
            save_on_db(json_response)
            # remake(json_response, query)


def save_on_db(tweets={}):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.hatemap
    collection = db.tweets
    post = {}
    for t in tweets['data']:
        if collection.count_documents({"_id": t['id']}) != 0:
            continue
        post['_id'] = t['id']
        post['author_id'] = t['id']
        post['raw_text'] = t['text']
        spacy_processed_text, spacy_entites = spacy_process(t['text'])
        post['spacy processed text'] = spacy_processed_text
        post['spacy entities'] = spacy_entites
        post['tag'] = tag(t['text'])
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
                    break

        collection.insert_one(post)


def spacy_process(tweet):
    # config = {
    #     "moves": None,
    #     "update_with_oracle_cut_size": 100,
    #     "model": DEFAULT_NER_MODEL,
    # }
    nlp = spacy.load("it_core_news_lg")
    # nlp.add_pipe("ner", config=config)

    doc = nlp(tweet)

    customize_stop_words = [
        'no',
        'non',
        'Non',
        'No'
    ]

    for w in customize_stop_words:
        nlp.vocab[w].is_stop = False

    lemmas_with_postag = []

    filtered_sentence = []
    for word in doc:
        lexeme = nlp.vocab[word.lemma_]
        if not lexeme.is_stop and not lexeme.is_space and not lexeme.is_punct:
            filtered_sentence.append(word)

    for token in filtered_sentence:
        lemmas_with_postag.append(token.lemma_ + " : " + token.pos_)

    entities = []

    for ent in doc.ents:
        entities.append(ent.text + " : " + ent.label_)

    return lemmas_with_postag, entities


def tag(raw_tweet):
    MyTagMe.GCUBE_TOKEN = "7f5391f2-142e-4fd5-9cc9-56e91c4c9add-843339462"

    annotations = MyTagMe.annotate(raw_tweet, lang="it", is_twitter_text=True)

    # Print annotations with a score higher than 0.1
    result = []
    for ann in annotations.get_annotations(0.1):
        result.append(ann.entity_id.__str__() + " : " + ann.entity_title + " : " + ann.uri(lang="it"))
    return result


if __name__ == "__main__":
    main()
