#!/usr/bin/env python3

"""
Find the word of interest.
"""

import sys
import json
import difflib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=argparse.FileType("r"))
args = parser.parse_args()

def diff(prev, cur):
    """
    I can't believe this isn't built into difflib.

    this is [-my-]{+your+} test of [-house-]{+houes+}
    """
    result = ""
    prev_action = ""
    buff = ""

    # print("/".join(difflib.ndiff(prev, cur)))

    actions = { "-": [], "+": [] }
    for diff in difflib.ndiff(prev.split(), cur.split()):
        action = diff[0]
        token = diff[2:]
        if action in actions.keys():
            actions[action].append(token)

    return " ".join(actions["-"]), " ".join(actions["+"])


data = json.load(args.infile)
for key, example in data.items():
    if "trg" in example:  # anaphora file
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
    else:
        for example in example["examples"]:
            correct_sent = example["trg"]["correct"][1]
            incorrect_sent = example["trg"]["incorrect"][1]

            correct_phrase, incorrect_phrase = diff(correct_sent, incorrect_sent)

            if correct_phrase in incorrect_sent:
                print("* WARNING", correct_phrase, "in", incorrect_sent, file=sys.stderr)
            if incorrect_phrase  in correct_sent:
                print("* WARNING", incorrect_phrase, "in", correct_sent, file=sys.stderr)

            example["correct-words"] = correct_phrase
            example["incorrect-words"] = incorrect_phrase

print(json.dumps(data, indent=2, ensure_ascii=False))
