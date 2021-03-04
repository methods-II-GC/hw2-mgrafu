#!/usr/bin/env python3
"""Tokenizes a corpus and splits into test, dev and training files.

This script takes a file as an imput, tokenizes it and randomizes it
to divide it into three files with names given in the command line.
These files will have 80%, 10% and 10% of the corpus content, respectively,
so the script can be used to create train, dev and test files.
"""

import argparse
import logging
import math
import random

from typing import Iterator, List, Tuple


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


def write_tags(source: List[List[List[str]]], path: str) -> Tuple[int, int]:
    lines_written = 0
    words_written = 0
    with open(path, "w") as target:
        for line in source:
            for word in line:
                statement = " ".join(word)
                print(statement, file=target)
                words_written += 1
            # To print blank lines after each sentence.
            print("", file=target)
            lines_written += 1
    # To log the file's statistics after writing.
    logging.info(
        "New file written:\n%s\nLines: %i\nTokens: %i\n",
        path,
        lines_written,
        words_written,
    )
    return lines_written, words_written


def main(args: argparse.Namespace) -> None:
    # This enables logging at INFO level.
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

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

    # These calculate a sum of the output statistics.
    total_lines = train_lines + dev_lines + test_lines
    total_tokens = train_tokens + dev_tokens + test_tokens
    logging.info("Total lines written: %i", total_lines)
    logging.info("Total tokens written: %i", total_tokens)

    # These print the info of the output files.
    if not args.verbose:
        title_template = "|{:12}|{:^7}|{:^8}|"
        row_template = "|{:12}|{:>7}|{:>8}|"
        separator = "{:-^31}".format("")
        print(title_template.format("File Name", "Lines", "Tokens"))
        print(separator)
        print(row_template.format(train_file_name, train_lines, train_tokens))
        print(row_template.format(dev_file_name, dev_lines, dev_tokens))
        print(row_template.format(test_file_name, test_lines, test_tokens))
        print(row_template.format("TOTAL", total_lines, total_tokens))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input", type=str, help="File name for the corpus to be used."
    )
    parser.add_argument(
        "train",
        type=str,
        help="File name for the training data file to be written.",
    )
    parser.add_argument(
        "dev", type=str, help="File name for the dev data file to be written."
    )
    parser.add_argument(
        "test",
        type=str,
        help="File name for the testing data file to be written.",
    )
    parser.add_argument(
        "--seed",
        required=True,
        help="PRNG seed to generate replicable results.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        const=True,
        default=False,
        action="store_const",
        help="Enable logging at info level",
    )

    main(parser.parse_args())
