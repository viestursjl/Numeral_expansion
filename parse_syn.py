import concurrent
from concurrent.futures import ALL_COMPLETED

import stanza
from stanza.utils.conll import CoNLL
import json
import time


CORPUS = "resources/LVK2022-v2-fixed-t2.5.3.vert"
TEMPFILE = "target/tempfile.txt"

POOL_SIZE = 8


# Reads a VERT file, line by line, and reconstructs sentences and paragraphs.
def vert_to_txt(vert):
    vert = vert.split("\n")
    text = ""
    output = ""

    for line in vert:
        line = line + "\n"
        if line == "\n":
            if text != "":
                output += (text + "\n")
            text = ""

        # Ja tiek nolasīts marķējuma simbols, veicam attiecīgās struktūras apstrādi.
        elif line[0] == "<" and line[1] != "\t":
            if line == "</doc>\n":
                continue
            elif line == "</p>\n":
                output += "\n"
                text = ""
            elif line == "</s>\n":
                output += "\n"
                text = ""
            elif line == "<g />\n" and len(text) > 1:
                continue
            else:
                continue
        else:
            output = output + line[:line.find("\t")]+" "
    return output


def clear_outputs():
    f = open("target/filter/num.txt", "a", encoding="utf-8")
    f.truncate(0)
    f = open("target/filter/both.txt", "a", encoding="utf-8")
    f.truncate(0)
    f = open("target/filter/full.txt", "a", encoding="utf-8")
    f.truncate(0)
    f.close()


# Šis ir tikai datu atlasei specifiskajam projektam.
def filter_texts(doc):
    with_numerals = []
    with_fullforms = []
    with_both = []
    for sentence in doc.sentences:
        contains_123 = False
        contains_one = False
        for token in sentence.tokens:
            if token.words[0].upos == "NUM":
                xpos = token.words[0].xpos
                if xpos.startswith("x") or xpos.startswith("y"):
                    contains_123 = True
                elif xpos.startswith("m"):
                    contains_one = True
                else:
                    contains_one = True
        if not contains_one and not contains_123:
            continue
        else:
            s = sentence.to_dict()
            if not contains_one:
                with_numerals.append(s)
            elif not contains_123:
                with_fullforms.append(s)
            else:
                with_both.append(s)

    if with_numerals:
        output = open("target/filter/num.txt", "a", encoding="utf-8")
        output.write(json.dumps(with_numerals, indent=4, ensure_ascii=False))
        with_numerals.clear()
        output.close()
    if with_fullforms:
        output = open("target/filter/full.txt", "a", encoding="utf-8")
        output.write(json.dumps(with_fullforms, indent=4, ensure_ascii=False))
        with_fullforms.clear()
        output.close()
    if with_both:
        output = open("target/filter/both.txt", "a", encoding="utf-8")
        output.write(json.dumps(with_numerals, indent=4, ensure_ascii=False))
        with_both.clear()
        output.close()


def process_stanza(text, doc_id):
    nlp = stanza.Pipeline('lv', download_method=None)   #, use_gpu=False)
    doc = nlp(text)
    try:
        filter_texts(doc)
    except Exception as error:
        print("Could not process text", error)
    CoNLL.write_doc2conll(doc, "target/conllu/"+doc_id+".conllu")


def multithread_stanza(doc_text, curr_doc_id):
    print("Reading "+curr_doc_id+"!")
    try:
        process_stanza(doc_text, curr_doc_id)
    except Exception as error:
        print("Could not parse "+curr_doc_id+" with Stanza!", error)
    print("Processed "+curr_doc_id+"!")


def read_doc(corpus):
    executor = concurrent.futures.ProcessPoolExecutor(POOL_SIZE)
    clear_outputs()

    line = corpus.readline()
    doc = line
    curr_doc_id = ""
    while True:
        if not line:
            break
        if line.startswith("<doc"):
            curr_doc_id = line.split("'")[1]
        doc += line
        if line.startswith("</doc>"):
            doc_text = vert_to_txt(doc)
            executor.submit(multithread_stanza, doc_text, curr_doc_id)
            doc = ""
        line = corpus.readline()


def main():
    stanza.download('lv')
    corpus = open(CORPUS, "r", encoding="utf-8")
    read_doc(corpus)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Executed in: {} seconds!".format(end - start))

