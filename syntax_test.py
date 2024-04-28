# Pynini library setup required Linux or Linux subsystem

import json
import pynini
from pynini.lib.rewrite import top_rewrite


def get_fst(far_path):
    return pynini.Far(far_path).get_fst()

fst_exp: pynini.Fst = get_fst("resources/expand.far")


text = "Sagaidāms, ka ASV Senāts jau otrdien apstiprinās lielu palīdzības paketi Ukrainai un citiem Savienoto Valstu sabiedrotajiem 95 miljardu dolāru apjomā, arī 61 miljarda dolāru vērtu palīdzību Ukrainai."
text1 = "... 95 miljardu apmērā ..."
text1 = "... deviņdesmit piec+UNK miljardu apmērā ..."
text1 = "... deviņdesmit piec+GENMAS miljardu apmērā ..."
text1 = "... deviņdesmit piecu miljardu apmērā ..."


def stanza_decline(sentence):

    return sentence


def syn_expand(sentence):
    sentence = sentence.replace("[", "\\[").replace("]", "\\]")
    phase1 = top_rewrite(sentence, fst_exp)
    phase1 = phase1.replace("\\[", "[").replace("\\]", "]")

    phase2 = stanza_decline(phase1)
    phase2 = phase2.replace("[", "\\[").replace("]", "\\]")

    phase3 = top_rewrite(phase2, fst_exp)
    phase3 = phase3.replace("\\[", "[").replace("\\]", "]")
    return
