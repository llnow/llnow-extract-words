import boto3
from janome.tokenizer import Tokenizer
import re


def split_texts_into_words(texts, bucket):
    # 除去する繰り返し表現をDynamoDBから取得
    table = boto3.resource('dynamodb').Table('ll-now-remove-repeat')
    res = table.scan()
    remove_repeat = [c['character'] for c in res['Items']]
    remove_repeat_pattern = '|'.join(['^(' + rr + '){2,}$' for rr in remove_repeat])  # 2回以上の繰り返しパターン

    # ユーザ辞書をs3からダウンロード
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    file_key = 'lovelive_word_dic.csv'
    file_path = '/tmp/lovelive_word_dic.csv'
    bucket.download_file(file_key, file_path)

    # ユーザ辞書を使う
    t = Tokenizer(file_path, udic_enc='utf-8')

    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞']:
                if not re.match(remove_repeat_pattern, token.base_form):
                    words.append(token.base_form)

    return words
