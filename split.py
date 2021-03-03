#!/usr/bin/env python3
"""Tokenizes a corpus and splits into test, dev and training files.

This script takes a file as an imput, tokenizes it and randomizes it
to divide it into three files with names given in the command line.
These files will have 80%, 10% and 10% of the corpus content, respectively,
so the script can be used to create train, dev and test files.
"""

import argparse
import math
import random

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
    lines_written = 0
    words_written = 0
    with open(path, "w") as target:
        for line in source:
            for word in line:
                statement = ' '.join(word)
                print(statement, file=target)
                words_written += 1
            # To print blank lines after each sentence.
            print('', file=target)
            lines_written += 1
    return lines_written, words_written

def main(args: argparse.Namespace) -> None:
    # These get the corpus as an iterator and its info.
    corpus_name = args.input
    corpus = list(read_tags(corpus_name))
    corpus_len = len(corpus)
    
    # These create a seeded PRNG just to shuffle the corpus.
    corpus_shuffler = random.Random(args.seed)
    corpus_shuffler.shuffle(corpus)
    
    # These get the info for the train file and write it.
    train_file_name = args.train
    train_file_EOF_corpus_index = math.floor(corpus_len / 10 * 8)
    train_file_data = corpus[:train_file_EOF_corpus_index]
    train_lines, train_tokens = write_tags(train_file_data, train_file_name)
    
    # These get the info for the dev file and write it.
    dev_file_name = args.dev
    dev_file_BOF_corpus_index = math.floor(corpus_len / 10 * 8)
    dev_file_EOF_corpus_index = math.floor(corpus_len / 10 * 9)
    dev_file_data = corpus[dev_file_BOF_corpus_index:dev_file_EOF_corpus_index]
    dev_lines, dev_tokens = write_tags(dev_file_data, dev_file_name)
    
    # These get the info for the test file and write it.
    test_file_name = args.test
    test_file_BOF_corpus_index = math.floor(corpus_len / 10 * 9)
    test_file_data = corpus[test_file_BOF_corpus_index:]
    test_lines, test_tokens = write_tags(test_file_data, test_file_name)
    
    #These calculate a sum of the output statistics.
    total_lines = train_lines + dev_lines + test_lines
    total_tokens = train_tokens + dev_tokens + test_tokens
    
    # These print the info of the output files.
    print("|{:12}|{:^7}|{:^8}|".format("File Name", "Lines", "Tokens"))
    print("{:-^31}".format("-"))
    print("|{:12}|{:>7}|{:>8}|".format(train_file_name, train_lines, train_tokens))
    print("|{:12}|{:>7}|{:>8}|".format(dev_file_name, dev_lines, dev_tokens))
    print("|{:12}|{:>7}|{:>8}|".format(test_file_name, test_lines, test_tokens))
    print("|{:12}|{:>7}|{:>8}|".format("TOTAL", total_lines, total_tokens))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="File name for the corpus to be used.")
    parser.add_argument("train", type=str, help="File name for the training data file to be written.")
    parser.add_argument("dev", type=str, help="File name for the dev data file to be written.")
    parser.add_argument("test", type=str, help="File name for the testing data file to be written.")
    parser.add_argument("--seed", required=True, help="PRNG seed to generate replicable results.")
    
    main(parser.parse_args())
