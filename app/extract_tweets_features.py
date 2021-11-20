from posted_time_utc2jst import *
import os
import boto3
import json

region = os.environ['AWS_DEFAULT_REGION']
ssm = boto3.client('ssm', region)


def extract_tweets_features(tweets, mode):
    n_tweet = len(tweets)
    latest_tweet_created_at = posted_time_utc2jst(tweets[0]['created_at'])
    oldest_tweet_created_at = posted_time_utc2jst(tweets[-1]['created_at'])
    tweets_features = json.dumps({
        "latest_tweet_created_at": latest_tweet_created_at,
        "n_tweet": n_tweet,
        "oldest_tweet_created_at": oldest_tweet_created_at
    })

    # tweets_featureをSystem Managerパラメータストアに記録
    key = 'll-now-tweets-features-{}'.format(mode)
    update_ssm_param(key, tweets_features)


def update_ssm_param(key, value):
    ssm.put_parameter(
        Name=key,
        Value=value,
        Overwrite=True
    )
