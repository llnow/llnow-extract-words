from fetch_tweets import *
from extract_tweets_features import *
from extract_texts import *
from split_texts_into_words import *
from put_words import *


def main(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    tweets = fetch_tweets(bucket, key)
    extract_tweets_features(tweets)
    texts = extract_texts(tweets)
    words = split_texts_into_words(texts, bucket)
    put_words(words, bucket)
