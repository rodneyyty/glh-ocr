import docx
import os
import re
import io
import json

from bs4 import BeautifulSoup
from gensim.models import Doc2Vec
from PyPDF2 import utils, PdfFileReader
from collections import defaultdict

MODEL = defaultdict(lambda: None)

LAWINSIDER_CLASSES = [
    u'employment-agreement'
    # , u'purchase-agreement'
    , u'stockholders-agreement'
    , u'loan-agreement'
    # , u'stock-option-agreement'
    # , u'license-agreement'
    # , u'underwriting-agreement'
    # , u'articles-of-incorporation'
    # , u'share-purchase-agreement'
    # , u'sale-and-purchase-agreement'
    # , u'share-exchange-agreement'
    # , u'financing-agreement'
    # , u'master-services-agreement'
    # , u'master-repurchase-agreement'
    # , u'repurchase-agreement'
]

REGEX_TYPES = [
    'employment agreement'
    # , 'purchase agreement'
    , 'stockholders agreement'
    , 'loan agreement'
    # , 'stock option agreement'
    # , 'license agreement'
    # , 'underwriting agreement'
    # , 'articles of incorporation'
    # , 'share purchase agreement'
    # , 'sale and purchase agreement'
    # , 'share exchange agreement'
    # , 'financing agreement'
    # , 'master services agreement'
    # , 'master repurchase agreement'
    # , 'repurchase agreement'
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


def predict_type(model, contract_toks):
    global MODEL
    if MODEL[model] is None:
        MODEL[model] = Doc2Vec.load(model)
    vec = MODEL[model].infer_vector(contract_toks)
    [(label, _)] = MODEL[model].docvecs.most_similar([vec], topn=1)
    return label


def dirPdfsToToks(dir_path):
    toks_list = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        toks = []
        if '.pdf' in file_name:
            try:
                input_pdf = PdfFileReader(open(file_path, 'rb'), strict=False)
                for page_idx in range(0, input_pdf.numPages):
                    toks += input_pdf.getPage(page_idx).extractText().split()
                if len(toks) > 0:
                    toks_list.append((file_name, toks))
            except OSError:
                print(OSError)
            except utils.PdfReadError:
                print(utils.PdfReadError)
        elif '.doc' in file_name:
            doc = docx.Document(file_path)
            toks = []
            for para in doc.paragraphs:
                toks += para.text.split()
            if len(toks) > 0:
                toks_list.append((file_name, toks))
    return toks_list


def find_first_type_match(lines):
    matchers = [re.compile('(' + type + ')', re.IGNORECASE) for type in REGEX_TYPES]
    for line in lines:
        match_results = [matcher.search(" ".join(line.split())) for matcher in matchers]
        for (idx, match) in enumerate(match_results):
            if match is not None:
                return REGEX_TYPES[idx]
    return None


def parse_text(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


def lawinsider_get_toks(file_path, pages=2):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        page_counter = 0
        query_html = ''
        for line in f.readlines():
            query_html += line
            try:
                if 'style="page-break-before:always"' in line:
                    page_counter += 1
                if page_counter == pages:
                    break
            except KeyError:
                pass
    toks = []
    for line in BeautifulSoup(query_html, "lxml").stripped_strings:
        toks += line.strip().split()
    return toks


def lawinsider_get_label(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())
        category = json_data['category']
        if category in LAWINSIDER_CLASSES:
            return category
        else:
            return 'OTHERS'
