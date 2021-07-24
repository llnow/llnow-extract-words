import re
import boto3


def extract_texts(tweets):
    # 除去する単語をDynamoDBから取得
    table = boto3.resource('dynamodb').Table('ll_now')
    primary_key = {"primary": 'remove_word'}
    res = table.get_item(Key=primary_key)
    remove_words = res['Item']['word']
    remove_words_pattern = '|'.join(remove_words)

    texts = []
    for tweet in tweets:
        text = tweet['text']
        hashtags = ['#' + ht['text'] for ht in tweet['entities']['hashtags']]
        hashtags_pattern = '|'.join(hashtags)
        # ハッシュタグを除去
        text = re.sub(hashtags_pattern, ' ', text)
        # URLを除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', ' ', text)
        # 改行を除去
        # text=re.sub('\n', ' ', text)
        # 絵文字などを除去
        text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', ' ', text)
        # 不要な単語を除去
        text = re.sub(remove_words_pattern, '', text)

        texts.append(text)

    return texts
