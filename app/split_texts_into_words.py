import boto3
import MeCab
import re


def split_texts_into_words(texts, bucket):
    # 除去する繰り返し表現をDynamoDBから取得
    table = boto3.resource('dynamodb').Table('ll-now-remove-repeat')
    res = table.scan()
    remove_repeat = [c['character'] for c in res['Items']]
    remove_repeat_pattern = '|'.join(['^(' + rr + '){2,}$' for rr in remove_repeat])  # 2回以上の繰り返しパターン

    # tokenizerを定義
    tagger = set_tokenizer()

    words = []
    for text in texts:
        node = tagger.parseToNode(text)
        while node:
            surface = node.surface
            pos = node.feature.split(',')[0]
            if (not node.feature.startswith('BOS/EOS')) and \
               (pos in ['名詞'] or re.match("[Α-ω・’'.]", surface)) and \
               (not re.match(remove_repeat_pattern, surface)):
                words.append(surface)

            node = node.next

    return words


def set_tokenizer():
    tagger = MeCab.Tagger(
        '-O wakati '
        '-r /dev/null '
        '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd '
        '-u /userdic.dic'
    )

    return tagger
