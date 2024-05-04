# pretrained doc2vec models on Japanese Wikipedia

This is a repository of doc2vec models trained on Japanese Wikipedia corpus.

Please See [my blog](https://yag-ays.github.io/project/pretrained_doc2vec_wikipedia/) for more details.

## Pretrained models

- `dbow300d`
  - https://www.dropbox.com/s/j75s0eq4eeuyt5n/jawiki.doc2vec.dbow300d.tar.bz2?dl=0
  - Compressed file size: 5.48 GB
- `dmpv300d`
  - https://www.dropbox.com/s/njez3f1pjv9i9xj/jawiki.doc2vec.dmpv300d.tar.bz2?dl=0
  - Compressed file size: 8.86 GB


## Training

### Procedure

```shell
$ asdf local python 3.10.13
$ python -m venv .venv --prompt doc2vec_ja
$ source .venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
```


```shell
$ python ./src/parse_cirrus.py -i /path/to/jawiki-20240422-cirrussearch-content.json.gz -o /path/to/20240422-cirrus_all.tsv.bz2
$ python ./src/train.py -i /path/to/20240422-cirrus_all.tsv.bz2
```



### Parameters

| param         | dbow300d | dmpv300d |
| :------------ | :------- | :------- |
| `dm`          | 0        | 1        |
| `vector_size` | 300      | 300      |
| `window`      | 15       | 10       |
| `alpha`       | 0.025    | 0.05     |
| `min_count`   | 5        | 2        |
| `sample`      | 1e-5     | 0        |
| `epochs`      | 20       | 20       |
| `dbow_words`  | 1        | 0        |

### Corpus

- [`jawiki-20240422-cirrussearch-content.json.gz`](https://dumps.wikimedia.org/other/cirrussearch/20240422/)

### Enviornments

- Tokenizer
  - mecab-python3: 1.0.9

- requirements
  - gensim: 3.7.0
  - numpy: 1.26.4
