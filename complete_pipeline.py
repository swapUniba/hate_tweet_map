import concurrent
from concurrent.futures import ThreadPoolExecutor
from feel_it import EmotionClassifier, SentimentClassifier
import spacy
from DataBase import DataBase
from EntityLinker import EntityLinker
from TwitterSearch import TwitterSearch
import time
import util


nlp = spacy.load("it_core_news_lg")


def main():
    start = time.time()

    print("[1/7] Configuring twitter API...")
    twitter_search = TwitterSearch()

    print("[2/7] Searching for tweets...")
    twitter_results = twitter_search.search()
    mongo_db = DataBase()

    print("[3/7] pre processing tweets...")
    pre_processed_tweets = util.pre_process_response(twitter_results)
    new_tweet = mongo_db.delete_tweets_already_saved(pre_processed_tweets)

    tag_me = EntityLinker()
    print("[4/7] performing natural language processing operation...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tweet in new_tweet:
            futures.append(executor.submit(process_text_with_spacy(tweet)))

    print("[5/7] performing sentiment analyses...")
    if len(new_tweet) > 0:
        emotion_classifier = EmotionClassifier()
        sentiment_classifier = SentimentClassifier()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tweet in new_tweet:
            futures.append(executor.submit(analyze_sentiment(tweet, emotion_classifier, sentiment_classifier)))

    print("[6/7] performing entity linking...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for t in new_tweet:
            futures.append(executor.submit(link_entity(t, tag_me)))

    print("[7/7] saving on db...")

    if len(new_tweet) > 0:
        mongo_db.save_many(new_tweet)

    end = time.time()
    print("done in: {}".format(end-start))


def link_entity(t, tag_me):
    t['tags'] = tag_me.tag(t['raw_text'])


def analyze_sentiment(tweet, emotion_classifier, sentiment_classifier):
    text = tweet['raw_text']
    hold_list = [text]
    sentiment_analyses = {'emotion': emotion_classifier.predict(hold_list),
                          'sentiment': sentiment_classifier.predict(hold_list)}

    tweet['sentiment'] = sentiment_analyses


def process_text_with_spacy(tweet):
    doc = nlp(tweet['raw_text'])
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

    tweet['spacy_processed_text'] = lemmas_with_postag
    tweet['spacy_entities'] = entities


if __name__ == "__main__":
    main()
