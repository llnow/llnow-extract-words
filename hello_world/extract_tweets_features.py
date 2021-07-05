from posted_time_utc2jst import *
import json


def extract_tweets_features(tweets):
    n_tweet = len(tweets)
    latest_tweet_created_at = posted_time_utc2jst(tweets[0]['created_at'])
    oldest_tweet_created_at = posted_time_utc2jst(tweets[-1]['created_at'])
    tweets_features = {}
    tweets_features['n_tweet'] = n_tweet
    tweets_features['latest_tweet_created_at'] = latest_tweet_created_at
    tweets_features['oldest_tweet_created_at'] = oldest_tweet_created_at

    # 取得したツイートの特徴をjsonファイルに出力
    json_path = '/tmp/tweets_features.json'
    with open(json_path, 'w') as f:
        json.dump(tweets_features, f, indent=4, ensure_ascii=False)
