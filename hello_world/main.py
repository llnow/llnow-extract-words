from extract_texts import *
from tokenize import *
from put_words import *


def main(event, context):
    texts = extract_texts(event)
    words = tokenize(texts)
    put_words(words)
