# Numeral expansion
Dažādu mašīnmācīšanās rīku metodes skaitļu izvēršanai kontekstā.

Šajā repozitorijā ir ievietoti kodu fragmenti, kas pielietoti sintaktiskās parsēšanas metodes un GPT modeļu izstrādē ar mērķi spēt veikt skaitļa vārdu izvēršanu latviešu valodas literatūras un periodikas tekstos.
___
resources mape: <br>
  Satur Thrax veidotos gramatiku failus, kuri nepieciešami datu kopas sagatavošanā un sintaktiskās metodes implementācijā:
  * **collapse.far**: veic galveno saīsinājumu savēršanu, kas pielietota automātiskās datu kopas izveidē.
  * **expand.far**: veic skaitļa vārdu izvēršanas loģiku, kas pielietota sintaktiskās metodes implementācijā.
<br>

Būtiskāki faili:
  * **evaluate.py**: izsauc izstrādāto metožu novērtēšanu uz izvēlēto datu kopu.
  * **syntax_test.py**: satur sintaktiskās metodes implementāciju.
  * **chatgpt_test.py**: satur ChatGPT modeļu API izsaukuma implementāciju.
<br>

Datu kopas izveides nolūkos izstrādātie faili:
  * **parse_syn.py**: atlasa no pilnā LVK2022 korpusa teikumus, kuri satur skaitļa vārdus, kā arī veic visiem LVK2022 tekstiem sintaktisko analīzi pielietojot multi-threading.
  * **split_data.py**: sadala skaitļu vārdus saturošo teksta failu treniņa, validācijas un testa datu kopās.
  * **reconstruct_sents.py**: saņemot teikumus sintaktiski marķētā formā atjauno teikumu oriģinālo tekstu, kā arī veic skaitļa vārdu savēršanu par skaitļiem.
<br>

Datu kopas analīzes nolūkos:
* **token_dep_analyze.py**: analizē cik daudz skaitļi paskaidro tekstvienības, kas satur locījuma un dzimtas informāciju.
