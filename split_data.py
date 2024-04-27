import re
import numpy as np
from sklearn.model_selection import train_test_split
import json

NUMERIC = re.compile('^[0-9\.]+$')
FILE = "D:\\Uni\\Magistrs\\_MAGISTRA_DARBS\\LVK2022\\LVK2022_analiize\\resources\\full.txt"

dataset = []
TRAIN = 9/10
VALID = 1/9
TEST = 1/10

TRAIN_FILE = "datasets/train.txt"
VALID_FILE = "datasets/valid.txt"
TEST_FILE = "datasets/test.txt"


# Clear previous data
def clear_output_file(file):
    out = open(file, 'w', encoding="utf-8")
    out.write("")
    out.close()


# Clear previous data
def clear_datasets():
    clear_output_file(TRAIN_FILE)
    clear_output_file(VALID_FILE)
    clear_output_file(TEST_FILE)
    return


# This function writes the split dataset sentences as a formatted file
def write_txt(data, file):
    out = open(file, 'a', encoding="utf-8")
    for sent in data:
        text = json.dumps(sent, ensure_ascii=False)
        out.write(text+"\n")
    out.close()


def distribute_data(data):
    train, test = train_test_split(data, train_size=TRAIN, test_size=TEST)
    train, valid = train_test_split(train, train_size=1-VALID, test_size=VALID)
    write_txt(train, TRAIN_FILE)
    write_txt(valid, VALID_FILE)
    write_txt(test, TEST_FILE)


def check_sent(sent):
    for token in sent:
        if NUMERIC.match(token["text"]):
            return False
    return True


def process_doc(doc, is_final):
    if is_final:
        distribute_data(dataset)
        dataset.clear()
        return
    for sent in doc:
        if check_sent(sent):
            dataset.append(sent)
            if len(dataset) >= 10_000:
                distribute_data(dataset)
                dataset.clear()


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
            process_doc(data, False)
            doc_data = "[\n"
        else:
            doc_data += line
        line = f.readline()
    if doc_data:
        data = json.loads(doc_data)
        process_doc(data, True)
    print("Processing complete!")


def main():
    process_file(FILE)


main()
