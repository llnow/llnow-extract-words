from fetch_tweets import *
from extract_tweets_features import *
from extract_texts import *
from split_texts_into_words import *
from put_words import *


def main(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    mode = context.invoked_function_arn.split(':')[-1]

    tweets = fetch_tweets(bucket, key)
    extract_tweets_features(tweets, mode)
    texts = extract_texts(tweets)
    words = split_texts_into_words(texts, bucket)
    put_words(words, bucket)
