import json


# IZVĒRŠANAS METODES
from chatgpt_test import gpt_expand
from syntax_test import syn_stat_expand
from syntax_test import syn_ml_expand

TEST_SET = "datasets/merged/example.txt"
mistakes = []


def output_mistakes(info):
    o = open("target/syn_mistakes.txt", "w", encoding="utf-8")
    o.truncate(0)
    o.write(info+"\n")
    print(mistakes)
    if mistakes:
        for sent in mistakes:
            if sent:
                print(sent)
                o.write(sent[0]+"\n")
                o.write(sent[1]+"\n\n")
    o.close()


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
    info = "Method accuracy on numeral expansion: {}% ({}/{})".format(score, correct, total)
    output_mistakes(info)
    print(info)


evaluate(syn_stat_expand)
