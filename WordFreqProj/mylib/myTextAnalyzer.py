from collections import Counter
import pandas as pd
from konlpy.tag import Okt


def load_corpus(datafile):
    if hasattr(datafile, "seek"):
        datafile.seek(0)
    return pd.read_csv(datafile)


def get_freq_word(corpus, target_col):
    okt = Okt()
    words = []

    for text in corpus[target_col].dropna():
        nouns = [w for w in okt.nouns(str(text)) if len(w) > 1]
        words.extend(nouns)

    return Counter(words)