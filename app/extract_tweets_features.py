from posted_time_utc2jst import *
import boto3
import json


def extract_tweets_features(tweets, search_metadata, bucket):
    n_tweet = len(tweets)
    latest_tweet_created_at = posted_time_utc2jst(tweets[0]['created_at'])
    oldest_tweet_created_at = posted_time_utc2jst(tweets[-1]['created_at'])
    tweets_features = json.dumps({
        "latest_tweet_created_at": latest_tweet_created_at,
        "n_tweet": n_tweet,
        "oldest_tweet_created_at": oldest_tweet_created_at,
        'search_metadata': search_metadata
    })

    s3 = boto3.resource('s3')
    key = 'tmp/tweets_features.json'
    res = s3.Object(bucket, key).put(Body=json.dumps(tweets_features, indent=4, ensure_ascii=False))
    print(res)
