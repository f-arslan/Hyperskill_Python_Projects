from collections import defaultdict
import random
from typing import Counter
from nltk.util import ngrams
import re

SENTENCE_RANGE = 10


class NLP:
    def __init__(self) -> None:
        name_of_file = input()
        self.total_tokens = NLP.open_read_file(name_of_file)
        self.trigrams = NLP.transform_to_trigrams(self.total_tokens)
        self.markov_chain = NLP.trigrams_dict(self)
        self.PUNCTUATIONS = [".", "?", "!"]
        self.sentence = []
        self.sentence_10 = []

    @staticmethod
    def open_read_file(n_file):
        with open(n_file, "r", encoding="utf-8") as f:
            return f.read().split()

    @staticmethod
    def transform_to_trigrams(to_token):
        return list(ngrams(to_token, 3))

    def trigrams_dict(self) -> defaultdict(list):
        markov_chain = defaultdict(list)
        for head, mid, tail in self.trigrams:
            markov_chain[head + " " + mid].append(tail)

        for head in markov_chain:
            markov_chain[head] = Counter(markov_chain[head]).most_common()

        return markov_chain

    def menu(self):
        for _ in range(SENTENCE_RANGE):
            NLP.create_sentence(self)
            self.sentence_10.append(self.sentence)
            self.sentence = []
        NLP.print_sentences(self)

    def print_sentences(self):
        for sentence in self.sentence_10:
            print(" ".join(sentence), sep="\n")

    def create_sentence(self):
        while True:
            head = random.choice(list(self.markov_chain.keys()))
            if (
                bool(re.match(r"[A-Z]", head[0]))
                and not bool(re.match(r"[?!.]", head.split()[0][-1]))
                and not bool(re.match(r"[!?.]", head.split()[1][-1]))
            ):
                break
        self.sentence.append(head)
        count = 2
        while True:
            last_word = head.split()[-1]
            tail = self.markov_chain[head][0][0]
            head = last_word + " " + tail
            self.sentence.append(tail)
            count += 1
            if count >= 5 and head[-1] in self.PUNCTUATIONS:
                break
            if count > 35:
                break


corpus = NLP()
corpus.menu()
