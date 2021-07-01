import boto3
import json
import re


def extract_texts(event):
    s3 = boto3.resource('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # s3からツイートを取得
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(key)
    response = obj.get()
    body = response['Body'].read()
    tweets = json.loads(body.decode('utf-8'))

    texts = []
    remove_words = ['lovelive', 'LoveLive', 'ラブライブ', 'Aqours', 'aqours', 'サンシャイン', '沼津', 'sunshine', '虹ヶ咲',
                    '虹ヶ咲学園スクールアイドル同好会', '同好会', 'Liella', 'スーパースター', 'ラブライバー', 'スクールアイドル', 'LoveLivestaff', 'スクフェス',
                    'スクスタ']
    for tweet in tweets:
        text = tweet['text']
        if text.startswith('RT '):
            continue
        # URLの除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', text)
        # 改行の除去
        # text=re.sub('\n', ' ', text)
        # 絵文字などの除去
        text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', '', text)
        for rm_word in remove_words:
            text = re.sub(rm_word, ' ', text)
        # print(text)
        # print('----------')
        texts.append(text)

    return texts
