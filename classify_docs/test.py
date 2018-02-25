import sys

from utility import dirPdfsToToks, predict_type


def main(args):
    contracts_toks = dirPdfsToToks(args[0])
    for (file_path, toks) in contracts_toks:
        prediction = predict_type(toks)
        print(file_path + ': ' + prediction)


if __name__ == "__main__":
    main(sys.argv[1:])
# python -u test.py test_corpus