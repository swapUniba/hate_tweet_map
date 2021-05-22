import concurrent
from concurrent.futures import ThreadPoolExecutor
from feel_it import EmotionClassifier, SentimentClassifier
import spacy
from DataBase import DataBase
from EntityLinker import EntityLinker
from TwitterSearch import TwitterSearch
import time
import util
from tqdm import tqdm


nlp = spacy.load("it_core_news_lg")


def main():
    start = time.time()

    print("[1/3] retrieving tweets to process from  database...")

    mongo_db = DataBase()
    twitter_to_process = mongo_db.extract_tweets_to_process()

    print("[2/3] instantiating necessary modules...")

    if len(twitter_to_process) > 0:
        emotion_classifier = EmotionClassifier()
        sentiment_classifier = SentimentClassifier()
        tag_me = EntityLinker()

    print("[3/3] processing tweets...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tweet in tqdm(twitter_to_process):
            futures.append(executor.submit(process_text_with_spacy(tweet)))
            futures.append(executor.submit(analyze_sentiment(tweet, emotion_classifier, sentiment_classifier)))
            futures.append(executor.submit(link_entity(tweet, tag_me)))
            tweet['processed'] = str(True)
            mongo_db.update_one(tweet)

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
