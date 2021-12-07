import boto3
import json


def fetch_tweets(bucket, key):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(key)
    response = obj.get()
    body = response['Body'].read()
    res = json.loads(body.decode('utf-8'))
    tweets, search_metadata = res['statuses'], res['search_metadata']

    return tweets, search_metadata
