import spacy
from spacy.lang.it.examples import sentences
from spacy.pipeline import morphologizer
import RuntimePos as rp

def check_female_name(token):

    with open('docs/nomif.txt', 'r') as f:
        myNames = [line.strip() for line in f]

    if token.lower() in myNames:
        return True
    else:
        return False


def articolo_nome(tweet):

    inclusive = 0.0
    for idx,(token,tag,det, morph) in enumerate(tweet):

        if tag == 'PROPN' and idx != 0:
            if tweet[idx-1][1] == 'DET':
                if 'Gender' in tweet[idx-1][3] and 'PronType' in tweet[idx-1][3]:
                    if tweet[idx-1][3]['Gender'] == 'Fem' and tweet[idx-1][3]['PronType'] == 'Art':
                       inclusive = -0.5
                       print("la regola 'Articolo + Nome proprio di donna' diminuisce l'inclusività")

    return inclusive


## token== word[0]
## tag == word[1]
## det == word[2]
## new_morph[pos]['gender']== word[3]['Gender']

def femaleName_maleAppos(tweet):
    inclusive = 0.0
    for idx, (token, tag, det, morph) in enumerate(tweet):
        if tag == 'PROPN' and check_female_name(token):
            print(tag, token)
            continue
        if tag == 'NOUN' and det == 'appos':
            print(tag, det, token)
            if 'Gender' in morph:
                if morph['Gender'] == 'Masc':
                    inclusive = - 0.25

    return inclusive


def art_donna_noun(tweet):
    inclusive= 0.0
    for idx,(token, tag, det, morph) in enumerate(tweet):
        if token == 'donna' and idx != 0:
            if tweet[idx+1][1] == 'NOUN' and tweet[idx+1][3]['Gender'] == 'Masc':
                inclusive = - 0.25


    return inclusive

def femaleSub_malePart(tweet):
    inclusive= 0.0
    for idx,(token, tag, det, morph) in enumerate(tweet):
        if tag == 'PROPN' or tag == 'NOUN' and det == 'nsubj':
            continue
        if tag == 'AUX' and det == 'aux':
            if 'Person' in morph:
                if morph['Person'] == '3' and morph['Number'] == 'Sing':
                    if tweet[idx+1][1] == 'VERB' and tweet[idx+1][2] == 'ROOT':
                        if 'Gender' in morph and 'VerbForm'in morph and 'Number' in morph:
                            if tweet[idx+1][3]['Gender'] == 'Masc' and tweet[idx+1][3]['VerbForm'] == 'Part' and morph['Number'] == 'Sing':
                                inclusive = - 0.25

    return inclusive

def article_inclusive(tweet):

    inclusive = 0.0
    for idx, (token, tag, det, morph) in enumerate(tweet):
        if tag == 'PRON' or tag == 'NOUN':
            if 'Gender' in morph:
               if morph['Gender'] == 'Masc':
                   if (idx+2 < len(tweet)):
                       if tweet[idx + 1][0] == '/' or tweet[idx + 1][0] == '\\':
                          if tweet[idx + 2][1] == 'PRON' or tweet[idx + 2][1] == 'NOUN' and morph[idx + 2]['Gender'] == 'Fem':
                             inclusive = 0.25

    return inclusive


if __name__ == "__main__":
    path = '../../data.json'
    nlp = spacy.load("it_core_news_lg")

    ## inclusivity for the whole dataset
    inclusive = 0.0
    sentences, ph = rp.runtimePos(path)
    for sentence, phrase in zip(sentences, ph):
        inclusive += articolo_nome(phrase)
        inclusive += femaleName_maleAppos(phrase)
        inclusive += art_donna_noun(phrase)
        inclusive += femaleSub_malePart(phrase)
        inclusive += article_inclusive(phrase)
        print(sentence)

        print(inclusive)


