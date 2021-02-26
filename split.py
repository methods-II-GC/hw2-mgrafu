#!/usr/bin/env python3
"""Tokenizes a corpus and splits into test, dev and training files.

This script takes a file as an imput, tokenizes it and randomizes it
to divide it into three files with names given in the command line.
These files will have 80%, 10% and 10% of the corpus content, respectively,
so the script can be used to create train, dev and test files.

To check for accuracy, the randomizer is seeded with the number ####.
"""

import argparse

from math import floor
from random import shuffle
from typing import Iterator, List


def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines

def write_tags(source: Iterator[List[List[str]]], path: str):
    with open(path, "w") as target:
        for line in source:
            for word in line:
                statement = ' '.join(word)
                print(statement, file=target)
            print('', file=target)

def main(args: argparse.Namespace) -> None:
    corpus_name = args.input
    corpus = list(read_tags(corpus_name))
    shuffle(corpus)
    corpus_len = len(corpus)
    
    train_file_name = args.train
    train_file_EOF_corpus_index = floor(corpus_len / 10 * 8)
    train_file_data = corpus[:train_file_EOF_corpus_index]
    write_tags(train_file_data, train_file_name)
    
    dev_file_name = args.dev
    dev_file_BOF_corpus_index = floor(corpus_len / 10 * 8)
    dev_file_EOF_corpus_index = floor(corpus_len / 10 * 9)
    dev_file_data = corpus[dev_file_BOF_corpus_index:dev_file_EOF_corpus_index]
    write_tags(dev_file_data, dev_file_name)

    test_file_name = args.test
    test_file_BOF_corpus_index = floor(corpus_len / 10 * 9)
    test_file_data = corpus[test_file_BOF_corpus_index:]
    write_tags(test_file_data, test_file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="File name for the corpus to be used.")
    parser.add_argument("train", type=str, help="File name for the training data file to be written.")
    parser.add_argument("dev", type=str, help="File name for the dev data file to be written.")
    parser.add_argument("test", type=str, help="File name for the testing data file to be written.")
    
    main(parser.parse_args())
