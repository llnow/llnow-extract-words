import re


def extract_texts(tweets):
    texts = []
    remove_words = ['lovelive', 'LoveLive', 'ラブライブ', 'Aqours', 'aqours', 'サンシャイン', '沼津', 'sunshine', '虹ヶ咲',
                    '虹ヶ咲学園スクールアイドル同好会', '同好会', 'Liella', 'スーパースター', 'ラブライバー', 'スクールアイドル', 'LoveLivestaff', 'スクフェス',
                    'スクスタ']
    for tweet in tweets:
        text = tweet['text']
        # 'RT 'で始まるツイートを除外
        # if text.startswith('RT '):
        #     continue
        # URLを除去
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', text)
        # 改行を除去
        # text=re.sub('\n', ' ', text)
        # 絵文字などを除去
        text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', '', text)
        for rm_word in remove_words:
            text = re.sub(rm_word, ' ', text)

        texts.append(text)

    return texts
