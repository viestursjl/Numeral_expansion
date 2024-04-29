from openai import OpenAI


def get_key(file):
    f = open(file, "r", encoding="utf-8")
    key = f.readlines()
    return key[0]


CLIENT = OpenAI(api_key=get_key("resources/api_key.txt"))


def gpt_expand(sentence):
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Expand all of the numerals and integers to match the spoken text:"
            },
            {
                "role": "user",
                "content": sentence
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content


text = "Sagaidāms, ka ASV Senāts jau otrdien apstiprinās lielu palīdzības paketi Ukrainai un citiem Savienoto Valstu sabiedrotajiem 95 miljardu dolāru apjomā, arī 61 miljarda dolāru vērtu palīdzību Ukrainai."
print(gpt_expand(text))
