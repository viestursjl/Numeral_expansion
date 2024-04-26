import numpy as np
from sklearn.model_selection import train_test_split
import json
import pynini

FILE = "D:\\Uni\\Magistrs\\_MAGISTRA_DARBS\\LVK2022\\LVK2022_analiize\\resources\\full.txt"
dataset = []


def get_fst(far_path):
    return pynini.Far(far_path).get_fst()

fst_exp: pynini.Fst = get_fst("expand.far")


def shorten(text):
    print("Call Pynini here!")
    return text


def process_sent(sentence):
    full_text = ""
    for token in sentence:
        full_text += ["text"]+" "
    full_text = full_text.strip()
    short_text = shorten(full_text)
    dataset.append([short_text, full_text])


def process_doc(doc):
    global int_id
    print(int_id)
    int_id += 1
    for sent in doc:
        process_sent(sent)


def process_file(ofile):
    f = open(ofile, "r", encoding="utf-8")
    line = f.readline()
    doc_data = ""
    while True:
        if not line:
            break
        if line == "][\n":
            doc_data += "]"
            data = json.loads(doc_data)
            process_doc(data)
            doc_data = "[\n"
        else:
            doc_data += line
        line = f.readline()
    if doc_data:
        data = json.loads(doc_data)
        process_doc(data)
    print("Processing complete!")


def main():
    process_file(FILE)


main()
