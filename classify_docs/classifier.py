import sys
from utility import get_abs_path_from_args, get_tagged_docs
from gensim.models.doc2vec import Doc2Vec


def main(args):
    [dir_arg] = get_abs_path_from_args(args, 1)
    train_corpus = get_tagged_docs(dir_arg)
    model = Doc2Vec(vector_size=300, min_count=2, epochs=10)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs, workers=24)
    model.save("lawinsider.model")


if __name__ == "__main__":
    main(sys.argv[1:])
# nohup python -u classifier.py ../data/lawinsider/ &> classifier.out &
