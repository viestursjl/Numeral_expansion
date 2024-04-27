# Pynini library setup required Linux or Linux subsystem

import json
import pynini
from pynini.lib.rewrite import top_rewrite


def get_fst(far_path):
    return pynini.Far(far_path).get_fst()

fst_col: pynini.Fst = get_fst("resources/collapse.far")


def shorten(text):
    try:
        short = top_rewrite(text, fst_col)
    except Exception as error:
        print("Could not process the following sentnece:")
        print(text + "\n")
        return False
    if short:
        short = short.replace("\\[", "[").replace("\\]", "]")
    return short


def process_sent(sentence):
    full_text = ""
    sent_data = json.loads(sentence)
    for token in sent_data:
        token_text = token["text"].replace("[", "\\[").replace("]", "\\]")
        full_text += +" "
    full_text = full_text.strip()
    short_text = shorten(full_text)
    if short_text:
        return [short_text, full_text]
    return


# This function writes the split dataset sentences as a formatted file
def write_file(data, file):
    out = open(file, 'w', encoding="utf-8")
    for sent in data:
        text = json.dumps(sent, ensure_ascii=False)
        out.write(text+"\n")
    out.close()


def read_dataset(file):
    ofile = file.split("/")[0]+"/merged/"+file.split("/")[1]
    sentences = []
    f = open(file, 'r', encoding="utf-8")
    line = f.readline()
    while True:
        if not line:
            break
        sent_set = process_sent(line)
        if sent_set:
            sentences.append()
        line = f.readline()
    write_file(sentences, ofile)
    print("Finished processing {}".format(file))


def main():
    read_dataset("datasets/test.txt")
    read_dataset("datasets/valid.txt")
    read_dataset("datasets/train.txt")


main()
