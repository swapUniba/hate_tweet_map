import concurrent
from concurrent.futures import ThreadPoolExecutor
from feel_it import EmotionClassifier, SentimentClassifier
import spacy
from DataBase import DataBase
from EntityLinker import EntityLinker
from TwitterSearch import TwitterSearch
import multiprocessing


def main():
    print("[1/7] Configuring twitter API...")
    twitter_search = TwitterSearch()

    print("[2/7] Searching for tweets...")
    twitter_results = twitter_search.search()
    mongo_db = DataBase()

    print("[3/7] pre processing tweets...")
    pre_processed_tweets = pre_process_response(twitter_results)
    new_tweet = mongo_db.delete_tweets_already_saved(pre_processed_tweets)

    tag_me = EntityLinker()
    print("[4/7] performing natural language processing operation...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tweet in new_tweet:
            futures.append(executor.submit(spacy_processing_text([tweet])))

    print("[5/7] performing sentiment analyses...")
    if len(new_tweet) > 0:
        emotion_classifier = EmotionClassifier()
        sentiment_classifier = SentimentClassifier()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tweet in new_tweet:
            futures.append(executor.submit(sentiment_analyzer(emotion_classifier, [tweet], sentiment_classifier)))

    print("[6/7] performing entity linking...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for t in new_tweet:
            futures.append(executor.submit(entity_linking(t, tag_me)))

    print("[7/7] saving on db...")
    if len(new_tweet) > 0:
        mongo_db.save(new_tweet)

    print("done")


def entity_linking(t, tag_me):
    t['tags'] = tag_me.tag(t['raw_text'])


def sentiment_analyzer(emotion_classifier, new_tweet, sentiment_classifier):
    for t in new_tweet:
        text = t['raw_text']
        hold_list = [text]
        sentiment_analyses = {'emotion': emotion_classifier.predict(hold_list),
                              'sentiment': sentiment_classifier.predict(hold_list)}

        t['sentiment'] = sentiment_analyses


def spacy_processing_text(new_tweet):
    for t in new_tweet:
        text = t['raw_text']
        spacy_processed_text, spacy_entities = spacy_process(text)
        t['spacy_processed_text'] = spacy_processed_text
        t['spacy_entities'] = spacy_entities


def pre_process_response(twitter_results=[]):
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
                        break
            tweets_processed.append(post)
    return tweets_processed


def spacy_process(tweet):
    nlp = spacy.load("it_core_news_lg")
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

    return lemmas_with_postag, entities


if __name__ == "__main__":
    main()
