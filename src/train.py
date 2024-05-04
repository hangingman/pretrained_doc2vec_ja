import argparse
import bz2
import logging

from gensim.models.doc2vec import Doc2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.setLevel(level=logging.INFO)


def count_lines_in_bz_file(file_path):
    with bz2.open(file_path, 'rt') as f:
        line_count = sum(1 for line in f)
    return line_count


def train(args):
    settings = {
        "dbow300d": {"vector_size": 300,
                     "epochs": 20,
                     "window": 15,
                     "min_count": 5,
                     "dm": 0,  # PV-DBOW
                     "dbow_words": 1,
                     "workers": 8},
        "dmpv300d": {"vector_size": 300,
                     "epochs": 20,
                     "window": 10,
                     "min_count": 2,
                     "alpha": 0.05,
                     "dm": 1,  # PV-DM
                     "sample": 0,
                     "workers": 8}
    }

    for setting_name, setting in settings.items():
        model = Doc2Vec(corpus_file=args.input, **setting)
        model.save(f"model/jawiki.doc2vec.{setting_name}.model")
        model.save_word2vec_format(f"model/jawiki.doc2vec.{setting_name}.model.bin",
                                   doctag_vec=True,
                                   prefix='ent_',
                                   binary=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="doc2vecをトレーニングする")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="""タイトルとテキストをLineSentence format化したファイルのパス 
                        e.g. 'data/20190114-cirrus-all-corpus.txt'""")
    args = parser.parse_args()
    train(args)
