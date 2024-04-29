# Pynini library setup required Linux or Linux subsystem

import json
import stanza
from ast import literal_eval
# import pynini
# from pynini.lib.rewrite import top_rewrite
#
#
# def get_fst(far_path):
#     return pynini.Far(far_path).get_fst()
#
# fst_exp: pynini.Fst = get_fst("resources/expand.far")


text = "Sagaidāms, ka ASV Senāts jau otrdien apstiprinās lielu palīdzības paketi Ukrainai un citiem Savienoto Valstu sabiedrotajiem 95 miljardu dolāru apjomā, arī 61 miljarda dolāru vērtu palīdzību Ukrainai."
text1 = "... 95 miljardu apmērā ..."
text1 = "... {{{deviņdesmit piec+UNK}}} miljardu apmērā ..."
text1 = "... 95+GENMAS miljardu apmērā ..."
text1 = "... deviņdesmit piecu miljardu apmērā ..."

text2 = "Līdz 2024. gada 20. maijam"
STATS_FILE = "target/stats.csv"


def load_stats(num_type, head):
    relevant = []

    f = open(STATS_FILE, "r", encoding="utf-8")
    line = f.readline()
    while True:
        if not line:
            break
        data = line.split("\"")
        token_info = literal_eval(data[1])
        if num_type in token_info[0] and head == token_info[1]:
            # relevant.append(token_info)
            target_tok = token_info[0]
            if "Case=" in target_tok and "Gender=" in target_tok:
                case = target_tok.split("Case=")[1][:3]
                gender = target_tok.split("Gender=")[1][:3]
                final = (case + gender).upper()
                print(final)
                return final
        line = f.readline()
    return "NOMMAS"


def fixed_stat_method(token, sentence):
    if "feats" in sentence[token]:
        num_type = sentence[token]["feats"]
        head = "_"
        head_id = int(sentence[token]["head"])-1
        if head_id >= 0:
            head_tok =  sentence[head_id]
            if "feats" in head_tok:
                head = head_tok["feats"]
            else:
                head = "_"
        load_stats(num_type, head)


def find_decl(token, sentence):
    print("ŌwŌ")


def stanza_decline(sentence, phase1):
    nlp = stanza.Pipeline('lv', download_method=None)
    sentence = nlp(sentence)

    for x in range(len(phase1)):
        if phase1[x].startswith("{{{"):
            sentence[x]
            find_decl(x, sentence)
    return sentence


def exp_tokens(part_exp):
    sent = part_exp.split(" ")
    merger = ""

    owo = []
    in_token = False
    for tok in sent:
        if tok.startswith("{{{"):
            in_token = True
        if not in_token:
            owo.append(tok)
        else:
            merger += tok + " "
        if tok.endswith("}}}"):
            merger = merger.strip()
            owo.append(merger)
            merger=""
            in_token = False
    return owo


def syn_expand(sentence):
    # sentence = sentence.replace("[", "\\[").replace("]", "\\]")
    # phase1 = top_rewrite(sentence, fst_exp)
    # phase1 = phase1.replace("\\[", "[").replace("\\]", "]")
    #
    # expandable_tokens = exp_tokens(phase1)
    # print(expandable_tokens)
    # exit(1)
    #
    # phase2 = stanza_decline(phase1)
    # phase2 = phase2.replace("[", "\\[").replace("]", "\\]")
    #
    # phase3 = top_rewrite(phase2, fst_exp)
    # phase3 = phase3.replace("\\[", "[").replace("\\]", "]")
    return

# syn_expand(text)
load_stats("NumType=Card", "Case=Acc|Gender=Masc|Number=Plur")
