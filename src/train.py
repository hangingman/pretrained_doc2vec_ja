import bz2
import pickle
import logging
import argparse

from tqdm import tqdm
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.setLevel(level=logging.INFO)


def count_lines_in_bz_file(file_path):
    with bz2.open(file_path, 'rt') as f:
        line_count = sum(1 for line in f)
    return line_count


def train(args):
    documents = []
    total_lines = count_lines_in_bz_file(args.input)
    with bz2.open(args.input, 'rt') as f:
        for line in tqdm(f, total=total_lines):
            l = line.strip().split("\t")
            title = l[0]
            text = l[1].split(" ")
            documents.append(TaggedDocument(text, [title]))

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
        model = Doc2Vec(documents=documents, **setting)
        model.save(f"model/jawiki.doc2vec.{setting_name}.model")
        model.save_word2vec_format(f"model/jawiki.doc2vec.{setting_name}.model.bin",
                                   doctag_vec=True,
                                   prefix='ent_',
                                   binary=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="doc2vecをトレーニングする")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="タイトルとテキストをTSV化したファイルのパス e.g. 'data/20190114cirrus_all.tsv.bz2'")
    args = parser.parse_args()
    train(args)
