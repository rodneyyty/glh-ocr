import glob2
import io, os
import sys

from collections import defaultdict
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from kitchen.text.converters import to_unicode
from utility import get_abs_path_from_args, lawinsider_get_toks, lawinsider_get_label


def main(args):
    corpus = []
    corpus_outfile = 'lawinsider.corpus'
    [dir_arg] = get_abs_path_from_args(args, 1)
    html_paths = glob2.glob(os.path.join(dir_arg, '**', '*.html'))
    class_counter = defaultdict(int)
    with io.open(corpus_outfile, 'w', encoding='utf-8') as out:
        for html_path in html_paths:
            json_path = html_path.replace('.html', '.json')
            toks = lawinsider_get_toks(html_path)
            label = lawinsider_get_label(json_path)
            if label is not None:
                class_counter[label] += 1
                out.write(to_unicode(' '.join([label] + toks) + '\n'))
                corpus.append(TaggedDocument(toks, [label]))
    print(str(class_counter))

    model = Doc2Vec(vector_size=300, min_count=1, epochs=3, workers=24)
    model.build_vocab(corpus)
    model.train(corpus, total_examples=model.corpus_count, epochs=3)
    model.save("lawinsider.model")


if __name__ == "__main__":
    main(sys.argv[1:])
# nohup python -u classifier.py /home/ccchia.2014/glh-ocr/data/lawinsider/ &> classifier.out &