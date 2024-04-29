import json


# IZVĒRŠANAS METODES
from chatgpt_test import gpt_expand


TEST_SET = "datasets/merged/example.txt"
mistakes = []


def output_mistakes():
    print("TODO: output mistakes")


def evaluate(method):
    correct = 0
    total = 0
    mistakes.clear()

    f = open(TEST_SET, "r", encoding="utf-8")
    sent = f.readline()
    while True:
        sent_data = json.loads(sent)
        total += 1
        # Izsaukt tikai vienu reizi, lai nepielietotu ChatGPT API vairākkārt
        expand = method(sent_data[0])
        if expand == sent_data[1]:
            correct += 1
        else:
            mistakes.append(expand)
            print(expand)
            print(sent_data[1])

    score = correct/total * 100
    print("Method accuracy on numeral expansion: {}% ({}/{})".format(score, correct, total))


evaluate(gpt_expand)
