#!/usr/bin/env python
"""Tokenizes a corpus and splits into test, dev and training files.

This script takes a file as an imput, tokenizes it and randomizes it
to divide it into three files with names given in the command line.
These files will have the corpus divided into 80%, 20% and 20%,
so the script can be used to create train, dev and test files.

To check for accuracy, the randomizer is seeded with the number ####.
"""

import argparse


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


def main(args: argparse.Namespace) -> None:
    corpus = list(read_tags("conll2000.tag"))
    print(corpus[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO: declare arguments.
    main(parser.parse_args())
