import os, sys

from utility import predict_type
from tika import parser


def main(args):
    dir_path = args[0]
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            toks = parser.from_file(file_path)['content'].split()
            print(file_name + ': ' + predict_type(toks))
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main(sys.argv[1:])
# python -u test.py test_corpus