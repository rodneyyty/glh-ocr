import docx
import os

from gensim.models import Doc2Vec
from PyPDF2 import utils,PdfFileReader

MODEL = None

CLASSES = [
    u'employment-agreement'
    , u'purchase-agreement'
    , u'stockholders-agreement'
    , u'loan-agreement'
    , u'stock-option-agreement'
    , u'license-agreement'
    , u'underwriting-agreement'
    , u'articles-of-incorporation'
    , u'share-purchase-agreement'
    , u'sale-and-purchase-agreement'
    , u'share-exchange-agreement'
    , u'financing-agreement'
    , u'master-services-agreement'
    , u'master-repurchase-agreement'
    , u'repurchase-agreement'
    , u'stockholder-agreement'
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


def get_label(json_data):
    category = json_data['category']
    if category in CLASSES:
        return category
    else:
        return 'OTHERS'


def predict_type(contract_toks):
    global MODEL
    if MODEL is None:
        MODEL = Doc2Vec.load('lawinsider.model')
    vec = MODEL.infer_vector(contract_toks)
    [(label, _)] = MODEL.docvecs.most_similar([vec], topn=1)
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
