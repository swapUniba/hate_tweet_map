import string
import it_core_news_lg
import requests
import json
import time

import spacy
from pymongo import MongoClient
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAPtPgEAAAAAoVlZ4I0szkcu4dL%2Bhqif%2F%2BF45Oo%3DJbvSo773bskLu1GexDv9Dq1HjuSjfSwfxgLdDXEdlPO5mKyE6G'

search_url = "https://api.twitter.com/2/tweets/search/all"


def next_page( next_token="", query={}):
    if next_token != "":
        query["next_token"] = next_token
    return query


def make_query(keywords = "", language = "it", place = "italia", place_country='IT', user=""):
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
        #query['place'] = place
        query['query'] += " place_country:" + place_country
        query['place.fields'] = "contained_within,country,country_code,full_name,geo,id,name,place_type"
        query['expansions'] = 'geo.place_id'


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
    nltk.download('stopwords')
    nltk.download('brown')
    nltk.download('names')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('universal_tagset')
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
            json_response = connect_to_endpoint(search_url, headers, next_page(next_token=response["meta"]["next_token"],query=query))
            print(json.dumps(json_response, indent=4, sort_keys=True))
            time.sleep(2)
            save_on_db(json_response)
            #remake(json_response, query)


def save_on_db(tweets={}):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.hatemap
    collection = db.tweets
    post = {}
    for t in tweets['data']:
        if collection.count_documents({"_id": t['id']}) != 0:
            continue
        post['_id'] = t['id']
        post['raw_text'] = t['text']
        post['spacy processed text'] = spacy_process2(t['text'])
        #post['nltk processed text'] = nltk_process(t['text'])
        if 'geo' in t:
            post['geo_id'] = t['geo']['place_id']
            for p in tweets['includes']['places']:
                if p['id'] == post['geo_id']:
                    post['country'] = p['country']
                    post['city'] = p['full_name']
                    break

        collection.insert_one(post)


def spacy_process2(tweet):
    nlp = spacy.load("it_core_news_lg")
    doc = nlp(tweet)

    customize_stop_words = [
        'no',
        'non',
        'Non'
    ]

    for w in customize_stop_words:
        nlp.vocab[w].is_stop = False
    result = []

    filtered_sentence = []
    for word in doc:
        lexeme = nlp.vocab[word.lemma_]
        if not lexeme.is_stop and not lexeme.is_space and not lexeme.is_punct:
            filtered_sentence.append(word)





    # # Remove punctuation
    # punctuations = "?:!.,;\""
    # for word in filtered_sentence:
    #     if word.text in punctuations:
    #         filtered_sentence.remove(word)

    for token in filtered_sentence:
        result.append(token.lemma_ + " : " + token.pos_)

    return result


def spacy_process(tweet):
    nlp = it_core_news_lg.load()
    customize_stop_words = [
        'no',
        'non',
        'Non'
    ]

    for w in customize_stop_words:
        nlp.vocab[w].is_stop = False

    doc = nlp(tweet)

    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)

    #Filter the stopword
    filtered_sentence =[]
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)

    # Remove punctuation
    punctuations = "?:!.,;"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)


    return filtered_sentence

# def nltk_process(tweet):
#     nltk_stop_words = nltk.corpus.stopwords.words('italian')
#     normalized_tokens = normalise(word_tokenize(tweet), verbose=False)
#     normalized_tokens_no_punct = [t for t in normalized_tokens if t.text not in string.punctuation]
#     text_without_stop_words = [t for t in normalized_tokens_no_punct if t not in nltk_stop_words]
#
#     stemmer_snowball = SnowballStemmer('italian')
#     result = []
#     for word in text_without_stop_words:
#         result.append(stemmer_snowball.stem(word))
#     return result




if __name__ == "__main__":
    main()