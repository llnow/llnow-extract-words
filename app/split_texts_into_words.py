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

    # 記号を含む単語リスト
    terms_contain_symbol = ["A・ZU・NA", "μ’s"]

    words = []
    for text in texts:
        words_tmp = []
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            surface = token.surface
            if pos in ['名詞'] or re.match("[Α-ω・’]", surface):
                if not re.match(remove_repeat_pattern, surface):
                    words_tmp.append(surface)

        # 記号を含む単語の処理
        terms = []
        for term in terms_contain_symbol:
            if term in text:
                terms.append(term)
        if terms:
            for term in terms:
                words_of_term = [token.surface for token in t.tokenize(term)]
                for i in range(len(words_tmp) - (len(words_of_term) - 1)):
                    if i >= len(words_tmp):
                        break
                    if words_tmp[i:i + len(words_of_term)] == words_of_term:
                        del words_tmp[i:i + len(words_of_term)]
                        words_tmp.insert(i, term)

        words += words_tmp

    return words
