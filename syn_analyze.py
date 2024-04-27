import json
import csv
import warnings

# FILE = "part.txt"
FILE = "D:\\Uni\\Magistrs\\_MAGISTRA_DARBS\\LVK2022\\LVK2022_analiize\\resources\\full.txt"
utok = {}
stats = {}
int_id = 0


def to_csv(info, outfile):
    with open("target/"+outfile, 'w', encoding="utf-8", newline='') as f:
        k = dict(sorted(info.items(), key=lambda item: -item[1]))
        w = csv.writer(f)
        w.writerows(k.items())
    print("File created!")


def add_tok(token, info):
    if token in info:
        info[token] += 1
    else:
        info[token] = 1


def process_sent(sentence):
    for token in sentence:
        if "xpos" in token:
            if token["xpos"].startswith("m"):
                add_tok(token["lemma"], utok)
                if token["xpos"].startswith("x") or token["xpos"].startswith("y"):
                    add_tok(str(["Error", "_"]), stats)
                    warnings.warn(str(token))
                else:
                    head = int(token["head"])-1
                    if head != -1:
                        head_tok = sentence[head]
                        if "feats" in head_tok:
                            add_tok(str([token["feats"], head_tok["feats"]]), stats)
                        else:
                            add_tok(str([token["feats"], "_"]), stats)
                    else:
                        add_tok(str([token["feats"], "_"]), stats)


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
    to_csv(utok, "utok.csv")
    to_csv(stats, "stats.csv")


main()
