import argparse
import bz2
import gzip
import json

import MeCab
from tqdm import tqdm


def count_lines_in_gzip_file(file_path):
    with gzip.open(file_path, 'rt') as f:
        line_count = sum(1 for line in f)
    return line_count


def parse(args):
    wakati = MeCab.Tagger("-O wakati")
    wakati.parse("")

    total_lines = count_lines_in_gzip_file(args.input)
    with gzip.open(args.input) as fin:
        with bz2.open(args.output, 'wt') as fout:
            for line in tqdm(fin, total=total_lines):
                json_line = json.loads(line)
                if "index" not in json_line:
                    title = json_line["title"]
                    text = json_line["text"]

                    if title and text:
                        print("\t".join([title, wakati.parse(text).strip()]), file=fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="wikipediaのデータセットをパースしてTSV化する")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="wikipediaのJSONファイルのパス e.g. 'data/jawiki-20190114-cirrussearch-content.json.gz'")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="タイトルとテキストをTSV化したファイルの出力先パス e.g. 'data/20190114cirrus_all.tsv.bz2'")
    args = parser.parse_args()
    parse(args)
