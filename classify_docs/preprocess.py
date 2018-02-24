import glob2
import io, os
import json
import sys

from bs4 import BeautifulSoup
from collections import defaultdict
from kitchen.text.converters import to_unicode
from utility import get_abs_path_from_args, get_label


def main(args):
    [dir_arg] = get_abs_path_from_args(args, 1)
    html_paths = glob2.glob(os.path.join(dir_arg, '**', '*.html'))
    class_counter = defaultdict(int)
    with io.open('lawinsider.corpus', 'w', encoding='utf-8') as out:
        for html_path in html_paths:
            with io.open(html_path, 'r', encoding='utf-8') as f_html, \
                 io.open(html_path.replace('.html', '.json'), 'r', encoding='utf-8') as f_json:
                words = []
                lines = BeautifulSoup(f_html.read(), "lxml").stripped_strings
                for line in lines:
                    line = line.lower().strip()
                    for word in line.split():
                        words.append(word.strip())
                json_data = json.loads(f_json.read())
                label = get_label(json_data)
                if len(words) > 10 and label is not None:
                    class_counter[label] += 1
                    out.write(to_unicode(' '.join([label] + words) + '\n'))
    print(str(class_counter))


if __name__ == "__main__":
    main(sys.argv[1:])
# nohup python -u preprocess.py /home/ccchia.2014/glh-ocr/data/lawinsider/ &> preprocess.out &