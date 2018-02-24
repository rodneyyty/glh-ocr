import os

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
