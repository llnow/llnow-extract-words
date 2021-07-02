import boto3


def put_words(words, bucket):
    s3 = boto3.resource('s3')
    # s3に単語リストをtsvファイルとしてアップロード
    file_path = 'tmp/words.tsv'
    res = s3.Object(bucket, file_path).put(Body=' '.join(words))
