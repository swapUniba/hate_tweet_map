import concurrent
import json
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import Dict, List

import requests
from feel_it import EmotionClassifier, SentimentClassifier
import spacy
from DataBase import DataBase
from EntityLinker import EntityLinker
from TwitterSearch import TwitterSearch
import time
import util
from tqdm import tqdm

nlp = spacy.load("it_core_news_lg")
emotion_classifier = EmotionClassifier()
sentiment_classifier = SentimentClassifier()


def main():
    start = time.time()

    print("[1/3] retrieving tweets to process from  database...")

    mongo_db = DataBase()
    tweets_to_process = mongo_db.extract_tweets_to_process()

    print("[2/3] instantiating necessary modules...")

    print("[3/3] processing tweets...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tweet in tweets_to_process:
            fut = executor.submit(process, tweet)
            fut.add_done_callback(finalize_process)
            futures.append(fut)

        for job in tqdm(as_completed(futures), total=len(futures)):
            pass

    end = time.time()
    print("done in: {}".format(end - start))


def finalize_process(fut: Future):
    tweet, spacy, link, sentit = fut.result()
    fell_it = feel_it_analyze_sentiment(tweet['raw_text'])
    tweet['spacy'] = spacy
    tweet['tags'] = link
    tweet['sentiment'] = {}
    tweet['sentiment']['sent-it'] = sentit
    tweet['sentiment']['feel-it'] = fell_it
    tweet['processed'] = str(True)
    mongo_db = DataBase()
    mongo_db.update_one(tweet)


def process(tweet: {}):
    text = tweet['raw_text']
    return tweet, process_text_with_spacy(text), link_entity(text), sentit_analyze_sentiment(text)


def link_entity(tweet: ""):
    tag_me = EntityLinker()
    t = {'tag_me': tag_me.tag(tweet)}
    return t


def sentit_analyze_sentiment(tweet: ""):
    data = "{\"texts\": [{\"id\": \"1\", \"text\": \""
    data += tweet + "\"}]}"
    url = "http://193.204.187.210:9009/sentipolc/v1/classify"
    json_response = requests.post(url, data=data.replace("\n", "").encode('utf-8')).json()
    if 'results' in json_response:
        sentiment_analyses = {'subjectivity': json_response['results'][0]['subjectivity'],
                              'polarity': json_response['results'][0]['polarity']}
        d = {'done': str(True), 'sentiment': sentiment_analyses}

        return d
    return {'done': str(False)}


def feel_it_analyze_sentiment(tweet: ""):
    hold_list = [tweet]
    try:
        sentiment_analyses: dict[str, str] = {'emotion': emotion_classifier.predict(hold_list)[0],
                                              'sentiment': sentiment_classifier.predict(hold_list)[0]}
        d = {'done': str(True), 'sentiment': sentiment_analyses}
    except:
        time.sleep(0.01)
        return feel_it_analyze_sentiment(tweet)

    return d


def process_text_with_spacy(tweet: ""):
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
        lemmas_with_postag.append(token.lemma_ + " POS : " + token.pos_ + " MORPH : " + token.morph.__str__())

    entities = []

    for ent in doc.ents:
        entities.append(ent.text + " : " + ent.label_)

    return {'processed_text': lemmas_with_postag, 'entities': entities}


if __name__ == "__main__":
    main()
