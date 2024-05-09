import json


# IZVĒRŠANAS METODES
from chatgpt_test import gpt_expand
# from syntax_test import syn_stat_expand
# from syntax_test import syn_ml_expand

TEST_SET = "datasets/merged/test.txt"
mistakes = []


def output_mistakes(info):
    o = open("target/mistakes/gpt_mistakes3.txt", "w", encoding="utf-8")
    o.truncate(0)
    o.write(info+"\n")
    if mistakes:
        for sent in mistakes:
            if sent:
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
        if not sent:
            break
        sent_data = json.loads(sent)
        total += 1
        # Izsaukt tikai vienu reizi, lai nepielietotu ChatGPT API vairākkārt
        expand = method(sent_data[0])
        print(total)
        if expand.lower().replace(" ", "") == sent_data[1].lower().replace(" ", ""):
            correct += 1
        else:
            mistakes.append([expand, sent_data[1]])
        sent = f.readline()

    score = correct/total * 100
    info = "Method accuracy on numeral expansion: {0:.2f}% ({1}/{2})".format(score, correct, total)
    output_mistakes(info)
    print(info)


evaluate(gpt_expand)
