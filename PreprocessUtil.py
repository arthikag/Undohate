from sklearn.feature_extraction.text import TfidfVectorizer

from pandas import DataFrame
import html
import re
import nltk
from nltk import SnowballStemmer
import emoji
import time

nltk.data.path.append('nltk_data/')


def run(df) -> DataFrame:
    # print("\nPreprocessing dataframe...")

    start_time = time.time()
    df = preprocess(df)
    end_time = time.time()

    # print("\nPre-process Finished! (" + str(end_time-start_time) + " seconds)")
    return df


def preprocess(df) -> DataFrame:
    df.tweet = df.tweet.str.lower()

    # print("\t--removing user tags")
    df.tweet = df.tweet.apply(clean_user_tags)

    # print("\t--removing links")
    df.tweet = df.tweet.apply(remove_links)

    # print("\t--decontracting words")
    df.tweet = df.tweet.apply(decontracted)

    # print("\t--replacing emojizzz with description")
    df.tweet = df.tweet.apply(replace_emoji_with_description)

    # print("\t--cleaning punctuation")
    df.tweet = df.tweet.apply(clean_punc)

    # print("\t--keeping just text")
    df.tweet = df.tweet.apply(keep_alpha)

    # print("\t--removing stopwords")
    df.tweet = df.tweet.apply(remove_stop_words)

    # print("\t--merging multiple spaces")
    df.tweet = df.tweet.apply(merge_multiple_character_occurrences)

    # print("\t--stemming tweets")
    df.tweet = df.tweet.apply(stem_tweets)

    return df


def stem_tweets(sentence):
    stemmer = SnowballStemmer("english")
    stem_sentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stem_sentence += stem
        stem_sentence += " "
    stem_sentence = stem_sentence.strip()
    return stem_sentence


def merge_multiple_character_occurrences(sentence):
    return re.sub(r'[^\w\s]|(.)(?=\1)', '', sentence)


def decontracted(sentence):
    # specific
    sentence = re.sub(r"won\'t", "will not", sentence)
    sentence = re.sub(r"can\'t", "can not", sentence)

    # general
    sentence = re.sub(r"n\'t", " not", sentence)
    sentence = re.sub(r"\'re", " are", sentence)
    sentence = re.sub(r"\'s", " is", sentence)
    sentence = re.sub(r"\'d", " would", sentence)
    sentence = re.sub(r"\'ll", " will", sentence)
    sentence = re.sub(r"\'t", " not", sentence)
    sentence = re.sub(r"\'ve", " have", sentence)
    sentence = re.sub(r"\'m", " am", sentence)
    return sentence


def remove_links(sentence):
    link = re.compile(r'(\w+://\S+)')
    clean_text = re.sub(link, ' ', str(sentence))
    return clean_text


def replace_emoji_with_description(sentence):
    tweet = emoji.demojize(html.unescape(sentence))
    tweet = tweet.replace(":", " ")
    tweet = tweet.replace("_", " ")
    tweet = ' '.join(tweet.split())
    tweet = html.escape(tweet)
    return tweet


def remove_stop_words(sentence):
    stop_words = nltk.corpus.stopwords.words('english')
    re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
    return re_stop_words.sub(" ", sentence)


# function to remove user tags
def clean_user_tags(sentence):
    clean = re.compile(r'(@[\w_-]+)')
    clean_text = re.sub(clean, ' ', str(sentence))
    return clean_text


# function to clean the word of any punctuation or special characters
def clean_punc(sentence):
    cleaned = re.sub(r'[?|!|\'|"|#]', r'', sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]', r' ', cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned


def keep_alpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent
