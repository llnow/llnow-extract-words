import re
import boto3


def extract_texts(tweets):
    # ラブライブ！シリーズの基本的な単語をDynamoDBから取得
    table = boto3.resource('dynamodb').Table('lovelive_words')
    tables = table.scan()
    remove_words_pattern = '|'.join(tables['Items'][0]['words'])

    texts = []
    for tweet in tweets:
        text = tweet['text']
        # 'RT 'で始まるツイートを除外
        # if text.startswith('RT '):
        #     continue
        # URLを除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', ' ', text)
        # 改行を除去
        # text=re.sub('\n', ' ', text)
        # 絵文字などを除去
        text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', ' ', text)
        # ラブライブ！シリーズの基本的な単語を除去
        text = re.sub(remove_words_pattern, ' ', text)

        texts.append(text)

    return texts
