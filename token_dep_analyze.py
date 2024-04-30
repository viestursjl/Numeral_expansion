from ast import literal_eval


token_dep = []
def get_tag(feats):
    if "Case=" in feats:
        case = feats.split("Case=")[1][:3]
    else:
        case = "NOM"
    if "Gender=" in feats:
        gender = feats.split("Gender=")[1][:3]
    else:
        gender = "MAS"
    final = "+" + (case + gender).upper()
    return final


def token_info(sentence):
    sentence = literal_eval(sentence)
    for token in sentence:
        if "xpos" in token:
            if token["xpos"].startswith("m"):
                tag = "+NOMMAS" # Default value
                if "feats" in token:
                    tag = get_tag(token["feats"])
                head = int(token["head"])-1
                if head != -1:
                    head_tok = sentence[head]
                    token_dep.append([head_tok, tag])
                else:
                    token_dep.append(["", tag])

def read_dataset(file):
    ofile = file.split("/")[0]+"/token_dep/"+file.split("/")[1]
    sentences = []
    f = open(file, 'r', encoding="utf-8")
    line = f.readline()
    while True:
        if not line:
            break
        token_info(line)
        line = f.readline()

    o = open(ofile, "w", encoding="utf-8")
    o.truncate(0)
    for combo in token_dep:
        o.write(str(combo)+"\n")
    o.close()
    token_dep.clear()
    print("Finished processing {}".format(file))


def main():
    read_dataset("datasets/test.txt")
    read_dataset("datasets/valid.txt")
    read_dataset("datasets/train.txt")


main()
