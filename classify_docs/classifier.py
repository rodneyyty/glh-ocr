import sys
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os, io


def main(args):
    corpus_file = args[0]
    if not os.path.isfile(corpus_file):
        exit(1)
    corpus = []
    with io.open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            label, words = line.split(' ', 1)
            corpus.append(TaggedDocument(words.strip().split(), [label]))
    model = Doc2Vec(vector_size=300, min_count=2, iter=3, workers=24)
    model.build_vocab(corpus)
    model.train(corpus, total_examples=model.corpus_count, epochs=10)
    model.save("lawinsider.model")


if __name__ == "__main__":
    main(sys.argv[1:])
# nohup python -u classifier.py /home/ccchia.2014/glh-ocr/data/lawinsider/ &> classifier.out &
# python classifier.py C:\Users\chongcher\Documents\glh-ocr\data\lawinsider_2
