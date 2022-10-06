#!/usr/bin/env python3

"""
Find the word of interest.
"""

import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=argparse.FileType("r"))
args = parser.parse_args()

data = json.load(args.infile)
for key, example in data.items():
    for trg in example["trg"]:
        if "semi-correct" in trg:
            correct_sent = set(trg["semi-correct"][1].split())
        else:
            correct_sent = set(trg["correct"][1].split())
        incorrect_sent = set(trg["incorrect"][1].split())
        in_common = correct_sent.intersection(incorrect_sent)

        correct_words = correct_sent - in_common
        incorrect_words = incorrect_sent - in_common

        for word in correct_words:
            assert word not in incorrect_sent

        for word in incorrect_words:
            assert word not in correct_sent

        trg["correct-words"] = list(correct_words)
        trg["incorrect-words"] = list(incorrect_words)

        # print("CORRECT", correct_words, "INCORRECT", incorrect_words)

print(json.dumps(data, indent=2, ensure_ascii=False))
