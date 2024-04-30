# Pynini library setup required Linux or Linux subsystem

import json
import stanza
from ast import literal_eval
import pynini
from pynini.lib.rewrite import top_rewrite


def get_fst(far_path):
    return pynini.Far(far_path).get_fst()

fst_exp: pynini.Fst = get_fst("resources/expand.far")


STATS_FILE = "target/stats.csv"


def load_stats(num_type, head):
    # relevant = []

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
                final = "+" + (case + gender).upper()
                print(final)
                return final
        line = f.readline()
    return "+NOMMAS"


def fixed_stat_method(token, sentence):
    if "feats" in sentence.to_dict()[0][token]:
        tok = sentence.to_dict()[0][token]
        num_type = tok["feats"]
        head = "_"
        head_id = int(tok["head"]) - 1
        if head_id >= 0:
            head_tok = sentence.to_dict()[0][head_id]
            if "feats" in head_tok:
                head = head_tok["feats"]
            else:
                head = "_"
        decl = load_stats(num_type, head)
        return decl


def stanza_decline(sentence, phase1):
    nlp = stanza.Pipeline('lv')
    sentence = nlp(sentence)

    for x in range(len(phase1)):
        if phase1[x].startswith("{{{"):
            decl = fixed_stat_method(x, sentence)
            phase1[x] = phase1[x].replace("+DECL", decl).strip("{{{").strip("}}}")
    return " ".join(phase1)


def exp_tokens(part_expanded):
    sent = part_expanded.split(" ")
    merger = ""

    sent_tokens = []
    in_token = False
    for tok in sent:
        if tok.startswith("{{{"):
            in_token = True
        if not in_token:
            sent_tokens.append(tok)
        else:
            merger += tok + " "
        if tok.endswith("}}}"):
            merger = merger.strip()
            sent_tokens.append(merger)
            merger = ""
            in_token = False
    return sent_tokens


def syn_expand(sentence):
    sent = sentence.replace("[", "\\[").replace("]", "\\]")
    phase1 = top_rewrite(sent, fst_exp)
    phase1 = phase1.replace("\\[", "[").replace("\\]", "]")

    expandable_tokens = exp_tokens(phase1)

    phase2 = stanza_decline(sentence, expandable_tokens)
    phase2 = phase2.replace("[", "\\[").replace("]", "\\]")

    phase3 = top_rewrite(phase2, fst_exp)
    phase3 = phase3.replace("\\[", "[").replace("\\]", "]")
    return


piemērs = "Līdz 2024. gada 20. maijam novērojams 23,5 procentu pieaugums"
print(syn_expand(piemērs))
