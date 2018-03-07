import os, sys

from collections import defaultdict
from utility import predict_type
from tika import parser


def get_labels_and_dir(root_dir):
    result = []
    for label in os.listdir(root_dir):
        path = os.path.join(root_dir, label)
        if os.path.isdir(path):
            result.append((label, path))
    return result


def main(args):
    dir_path = args[0]
    model = args[1]
    if not os.path.isfile(model) or not os.path.isdir(dir_path):
        exit(0)
    results = defaultdict(lambda: defaultdict(int))
    for (label, test_dir) in get_labels_and_dir(dir_path):
        label_result = results[label]
        for file_name in os.listdir(test_dir):
            file_path = os.path.join(test_dir, file_name)
            toks = parser.from_file(file_path)['content'].split()
            prediction = predict_type(model, toks)
            label_result[prediction] += 1
    for label in sorted(results.keys()):
        print('Label: ' + label)
        label_result = results[label]
        for predicted_label in sorted(label_result, key=lambda x: label_result[x], reverse = True):
            print('\t' + predicted_label + ': ' + str(label_result[predicted_label]))
        print('\n')


if __name__ == "__main__":
    main(sys.argv[1:])
# python -u test.py ../data/type_classification_test/ lawinsider.model