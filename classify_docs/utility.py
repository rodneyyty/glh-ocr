import json
import os
from bs4 import BeautifulSoup
from gensim.models.doc2vec import TaggedDocument

CLASSES = [
    'employment agreement'
    , 'purchase agreement'
    , 'stockholders agreement'
    , 'loan agreement'
    , 'stock option agreement'
    , 'license agreement'
    , 'underwriting agreement'
    , 'articles of incorporation'
    , 'share purchase agreement'
    , 'sale and purchase agreement'
    , 'share exchange agreement'
    , 'financing agreement'
    , 'master services agreement'
    , 'master repurchase agreement'
    , 'repurchase agreement'
    , 'stockholder agreement'
]


def get_abs_path_from_args(args, expected_paths):
    result = []
    for arg in args:
        if os.path.isdir(arg):
            result.append(arg)
        else:
            result.append(os.path.abspath(arg))
    if len(result) == expected_paths:
        return result
    else:
        print('expected paths: ' + str(expected_paths))
        print('found: ' + str(len(result)) + ' ' + str(result))
        quit(1)


def get_file_paths(path):
    file_paths = []
    for root, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if '.html' in file_name:
                file_basename = os.path.join(root, file_name.replace('.html', ''))
                html_file_path = file_basename + '.html'
                json_file_path = file_basename + '.json'
                if os.path.isfile(html_file_path) and os.path.isfile(json_file_path):
                    file_paths.append(file_basename)
        for path in dir_names:
            file_paths += get_file_paths(os.path.join(root, path))
    return file_paths


def get_label(json_data):
    category = json_data['category']
    if category in CLASSES:
        return category
    else:
        return 'OTHERS'


def get_tagged_docs(path):
    samples = []
    labels = []
    for file_path in get_file_paths(path):
        with open(file_path + '.html') as f_html:
            samples.append(' '.join(BeautifulSoup(f_html.read(), "lxml").stripped_strings))
        with open(file_path + '.json') as f_json:
            json_data = json.loads(f_json.read())
            labels.append(get_label(json_data))
    tagged_docs = []
    print('sample len: ' + str(len(samples)))
    print('labels len: ' + str(len(labels)))
    for sample, label in zip(samples, labels):
        tagged_docs.append(TaggedDocument(sample, [label]))
