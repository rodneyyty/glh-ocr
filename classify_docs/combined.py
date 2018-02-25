import glob2
import io, os
import json
import sys

from bs4 import BeautifulSoup
from collections import defaultdict
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from kitchen.text.converters import to_unicode
from utility import get_abs_path_from_args, get_label


def main(args):
    corpus_outfile = 'lawinsider_front.corpus'
    [dir_arg] = get_abs_path_from_args(args, 1)
    html_paths = glob2.glob(os.path.join(dir_arg, '**', '*.html'))
    class_counter = defaultdict(int)
    with io.open(corpus_outfile, 'w', encoding='utf-8') as out:
        for html_path in html_paths:
            with io.open(html_path, 'r', encoding='utf-8') as f_html, \
                    io.open(html_path.replace('.html', '.json'), 'r', encoding='utf-8') as f_json:
                words = []
                soup = BeautifulSoup(f_html.read(), "lxml")
                lines = []
                divs = soup.find_all('div')
                for div in divs:
                    if div.string is None:
                        continue
                    elif not div.has_attr('id') or (div['id'] != 'PGBRK' and div['id'] != u'PGBRK'):
                        lines.append(div)
                    else:
                        for line in lines:
                            line = line.string.lower().strip()
                            for word in line.split():
                                words.append(word.strip())
                json_data = json.loads(f_json.read())
                label = get_label(json_data)
                if len(words) > 10 and label is not None:
                    class_counter[label] += 1
                    out.write(to_unicode(' '.join([label] + words) + '\n'))
    print(str(class_counter))

    corpus = []
    with io.open(corpus_outfile, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            label, words = line.split(' ', 1)
            corpus.append(TaggedDocument(words.strip().split(), [label]))
    model = Doc2Vec(size=300, min_count=2, iter=3, workers=24)
    model.build_vocab(corpus)
    model.train(corpus, total_examples=model.corpus_count, epochs=3)
    model.save("lawinsider.model")


if __name__ == "__main__":
    main(sys.argv[1:])
# nohup python -u combined.py /home/ccchia.2014/glh-ocr/data/lawinsider/ &> lawinsider_front.out &