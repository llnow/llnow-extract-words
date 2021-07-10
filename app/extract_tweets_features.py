from posted_time_utc2jst import *
import boto3


def extract_tweets_features(tweets):
    n_tweet = len(tweets)
    latest_tweet_created_at = posted_time_utc2jst(tweets[0]['created_at'])
    oldest_tweet_created_at = posted_time_utc2jst(tweets[-1]['created_at'])

    # tweets_featureをdynamodbに記録
    table = boto3.resource('dynamodb').Table('ll_now')
    try:
        table.update_item(
            Key={'primary': 'tweets_feature'},
            UpdateExpression="set feature.n_tweet=:nt, feature.latest_tweet_created_at=:ltca, "
                             "feature.oldest_tweet_created_at=:otca",
            ExpressionAttributeValues={
                ':nt': n_tweet,
                ':ltca': latest_tweet_created_at,
                ':otca': oldest_tweet_created_at
            },
            ReturnValues="UPDATED_NEW"
        )

    except Exception as e:
        print(e)
