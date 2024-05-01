# Pynini library setup required Linux or Linux subsystem

import json
import stanza
from ast import literal_eval
import pynini
from pynini.lib.rewrite import top_rewrite


def get_fst(far_path):
    return pynini.Far(far_path).get_fst()


fst_exp: pynini.Fst = get_fst("resources/expand.far")

# ================================================================
# Static method for declension choice

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


"""
:param token = pozīcija izvēršamajam tokenam teikumā
:param sentence = teikums stanza formātā
"""
def fixed_stat_method(token, sentence):
    if len(sentence.to_dict()[0]) < token:
        # FIXME: Šis ir brutāls ielāps, gadījumam, ja Stanza parsētājs nepareizi nosaka tokenu skaitu.
        print("Parsing error!")
        return "+NOMMAS"
    tok = sentence.to_dict()[0][token]
    num_type = ""
    if "feats" in sentence.to_dict()[0][token]:
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


# ================================================================
# Machine learning based approach to declension choice

# import torch
# import torchvision
# import torchvision.transforms as transforms
# # PyTorch TensorBoard support
# from torch.utils.tensorboard import SummaryWriter
# from datetime import datetime
#
#
# def model_training():
#     transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
#     batch_size = 4


"""
:param token = pozīcija izvēršamajam tokenam teikumā
:param sentence = teikums stanza formātā
"""
def ml_method(token, sentence):
    print("WIP")


# ================================================================
# Main syntactic declension logic

def stanza_decline(sentence, phase1, method):
    nlp = stanza.Pipeline('lv')
    sentence = nlp(sentence)

    for x in range(len(phase1)):
        if phase1[x].startswith("{{{"):
            decl = method(x, sentence)
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


def syn_expand(sentence, method):
    sent = sentence.replace("[", "\\[").replace("]", "\\]")
    phase1 = top_rewrite(sent, fst_exp)
    phase1 = phase1.replace("\\[", "[").replace("\\]", "]")

    expandable_tokens = exp_tokens(phase1)

    phase2 = stanza_decline(sentence, expandable_tokens, method)
    phase2 = phase2.replace("[", "\\[").replace("]", "\\]")

    phase3 = top_rewrite(phase2, fst_exp)
    phase3 = phase3.replace("\\[", "[").replace("\\]", "]")
    return phase3


def syn_stat_expand(sentence):
    return syn_expand(sentence, fixed_stat_method)


def syn_ml_expand(sentence):
    return syn_expand(sentence, ml_method)


piemērs = "Līdz 2024. gada 20. maijam novērojams 23,5 procentu pieaugums"
print(syn_expand(piemērs, fixed_stat_method))
