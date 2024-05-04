import argparse
import gzip
import json

import MeCab
from tqdm import tqdm


def count_lines_in_gzip_file(file_path):
    with gzip.open(file_path, 'rt') as f:
        line_count = sum(1 for line in f)
    return line_count


def parse(args):
    wakati: MeCab.Tagger = MeCab.Tagger("-O wakati")
    wakati.parse("")

    total_lines = count_lines_in_gzip_file(args.input)
    with open(args.output, mode='wt', encoding='utf8') as fout:
        with gzip.open(args.input) as fin:
            for line in tqdm(fin, total=total_lines):
                json_line = json.loads(line)
                if "index" not in json_line:
                    title = json_line["title"]  # SENTENCE_IDENTIFIER
                    text = json_line["text"]
                    words = [line for line in wakati.parse(text).strip().split(" ")]
                    line_sentence = [title] + words
                    fout.write(" ".join(line_sentence))
                    fout.write("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="wikipediaのデータセットをパースしてLineSentence formatで保存する")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="wikipediaのJSONファイルのパス e.g. 'data/jawiki-20190114-cirrussearch-content.json.gz'")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="""タイトルとテキストをLineSentence format化したファイルの出力先パス
                        e.g. 'data/20190114-cirrus-all-corpus.txt'""")
    args = parser.parse_args()
    parse(args)
