import re
import boto3
import unicodedata


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
        # 自身を包含する別のハッシュタグの一部を除去しないようにソート
        hashtags.sort(key=len, reverse=True)

        # ハッシュタグを除去
        if hashtags:
            hashtags_pattern = '|'.join(hashtags)
            text = re.sub(hashtags_pattern, ' ', text)
        # URLを除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', ' ', text)
        # 改行を除去
        # text=re.sub('\n', ' ', text)
        # Unicode正規化
        text = unicodedata.normalize('NFKC', text)
        # 半角のシングルクォーテーションを全角に変換
        text = re.sub(r"'", "’", text)
        # 絵文字などを除去
        text = re.sub(r"[^-,.、。!?ー〜×0-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕・Α-ω’]", " ", text)
        # 不要な単語を除去
        text = re.sub(remove_words_pattern, '', text)

        # ツイートを跨いでコロケーション判定されないように末尾にターミネータを付加
        text += ' eotw'

        texts.append(text)

    return texts
