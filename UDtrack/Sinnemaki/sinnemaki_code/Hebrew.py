from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

def possessive(conllu_item, returntype=list):
    try:
        analyses = conllu_item['analyysit']
    except TypeError:
        print(conllu_item)
        return {'dep_marked':[], 'head_marked':[], 'double_marked':[], 'zero_marked':[], 'head_exist':[]}

    sent_id = conllu_item['sent_id']

    def find_head_index(analysis):
        head_str = analysis[6]
        head_i = int(head_str)-1
        return head_i


    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []
    head_exist = []

    for a in analyses: # It seems like there is nothing but dependent-marking in the material
        #print('a in analyses, a =', a)
        # here a is dependent
        if a[3] == 'PRON' and 'PronType=Prs' in a[5] and a[7] == 'nmod:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)
        # a is particle
        elif a[2] == 'של' and a[3] == 'ADP' and 'Case=Gen' in a[5]:# and a[7] == 'nmod:poss':
            dep_i = find_head_index(a)
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and dep[7] == 'nmod:poss':
                    head_i = find_head_index(dep)
                    if head_i >= 0:
                        if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(dep)
    
    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = 3465
# text = אולפני ההסרטה של מ-ג-מ, שנפתחו לקהל ב9891 סמוך לפארקים האחרים בשטח של דיסני באורלנדו, כבר מדיפים ריח של נפטלין, במונחים אמריקאיים.
1	אולפני	אולפן	NOUN	NOUN	Definite=Cons|Gender=Masc|Number=Plur	33	nsubj	_	_
2-3	ההסרטה	_	_	_	_	_	_	_	_
2	ה	ה	DET	DET	PronType=Art	3	det:def	_	_
3	הסרטה	הסרטה	NOUN	NOUN	Gender=Fem|Number=Sing	1	compound:smixut	_	_
4	של	של	ADP	ADP	Case=Gen	5	case:gen	_	_
5	מ	מ	PROPN	PROPN	_	1	nmod	_	SpaceAfter=No
6	-	-	PUNCT	PUNCT	_	5	flat:name	_	SpaceAfter=No
7	ג	ג	PROPN	PROPN	_	5	flat:name	_	SpaceAfter=No
8	-	-	PUNCT	PUNCT	_	5	flat:name	_	SpaceAfter=No
9	מ	מ	PROPN	PROPN	_	5	flat:name	_	SpaceAfter=No
10	,	,	PUNCT	PUNCT	_	1	punct	_	_
11-12	שנפתחו	_	_	_	_	_	_	_	_
11	ש	ש	SCONJ	SCONJ	_	12	mark	_	_
12	נפתחו	נפתח	VERB	VERB	Gender=Fem,Masc|HebBinyan=NIFAL|Number=Plur|Person=3|Tense=Past|Voice=Mid	1	acl:relcl	_	_
13-15	לקהל	_	_	_	_	_	_	_	_
13	ל	ל	ADP	ADP	_	15	case	_	_
14	ה_	ה	DET	DET	PronType=Art	15	det:def	_	_
15	קהל	קהל	NOUN	NOUN	Gender=Masc|Number=Sing	12	obl	_	_
16-17	ב9891	_	_	_	_	_	_	_	_
16	ב	ב	ADP	ADP	_	17	case	_	_
17	9891	9891	NUM	NUM	_	12	obl	_	_
18	סמוך	_	ADV	ADV	_	12	advmod	_	_
19-21	לפארקים	_	_	_	_	_	_	_	_
19	ל	ל	ADP	ADP	_	21	case	_	_
20	ה_	ה	DET	DET	PronType=Art	21	det:def	_	_
21	פארקים	פארק	NOUN	NOUN	Gender=Masc|Number=Plur	18	fixed	_	_
22-23	האחרים	_	_	_	_	_	_	_	_
22	ה	ה	DET	DET	PronType=Art	23	det:def	_	_
23	אחרים	אחר	ADJ	ADJ	Gender=Masc|Number=Plur	21	amod	_	_
24-26	בשטח	_	_	_	_	_	_	_	_
24	ב	ב	ADP	ADP	_	26	case	_	_
25	ה_	ה	DET	DET	PronType=Art	26	det:def	_	_
26	שטח	שטח	NOUN	NOUN	Gender=Masc|Number=Sing	12	obl	_	_
27	של	של	ADP	ADP	Case=Gen	28	case:gen	_	_
28	דיסני	דיסני	PROPN	PROPN	_	26	nmod	_	_
29-30	באורלנדו	_	_	_	_	_	_	_	SpaceAfter=No
29	ב	ב	ADP	ADP	_	30	case	_	_
30	אורלנדו	אורלנדו	PROPN	PROPN	_	26	nmod	_	_
31	,	,	PUNCT	PUNCT	_	33	punct	_	_
32	כבר	כבר	ADV	ADV	_	33	advmod	_	_
33	מדיפים	הדיף	VERB	VERB	Gender=Masc|HebBinyan=HIFIL|Number=Plur|Person=1,2,3|VerbForm=Part|Voice=Act	0	root	_	_
34	ריח	ריח	NOUN	NOUN	Gender=Masc|Number=Sing	33	obj	_	_
35	של	של	ADP	ADP	Case=Gen	36	case:gen	_	_
36	נפטלין	נפטלין	NOUN	NOUN	Gender=Masc|Number=Sing	34	nmod:poss	_	SpaceAfter=No
37	,	,	PUNCT	PUNCT	_	39	punct	_	_
38-39	במונחים	_	_	_	_	_	_	_	_
38	ב	ב	ADP	ADP	_	39	case	_	_
39	מונחים	מונח	NOUN	NOUN	Gender=Masc|Number=Plur	33	obl	_	_
40	אמריקאיים	אמריקני	ADJ	ADJ	Gender=Masc|Number=Plur	39	amod	_	SpaceAfter=No
41	.	.	PUNCT	PUNCT	_	33	punct	_	_'''

conllu_item = to_ordered_dict(test)
d = possessive(conllu_item, dict)

if __name__ == '__main__':
    if type(d) == dict:
        for item in d:
            print(item, d[item])
    else:
        for item in d:
            print(item)


def str2poss(s, returntype=dict):
    conllu_item = to_ordered_dict(s)
    return possessive(conllu_item, returntype)

def str2bea(s, returntype=dict):
    d = str2poss(s, returntype)
    if type(d) == dict:
        for item in d:
            print(item, d[item], len(d[item]))
    else:
        for item in d:
            print(item)

def str2beastr(s):
    d = str2poss(s, dict)
    answer = []
    for item in d:
        answer.append('{} {} {}'.format(item, d[item], len(d[item])))
    return '\n'.join(answer)


def strip_indent(s, i=1):
    c = []
    for j in s.splitlines():
        c.append(j[4*i:])
    return '\n'.join(c)
        
if __name__ == '__main__':
    exec(r'''import os

while 'UDtrack' in os.listdir():
    os.chdir('UDtrack')

folders = [w for w in os.listdir() if LANGUAGE in w and '.' not in w]

rootfolder = os.getcwd()

answer = ''

for folder in folders:
    os.chdir(folder)
    files = os.listdir()
    if folder[3:] + '_THIS.conllu' in files:
        file = folder[3:] + '_THIS.conllu'
        # A final modified file should be have a name that ends with
        # _THIS.conllu
        # e.g. UD_Afrikaans-AfriBooms_THIS.conllu
    else:
        file = folder[3:] + '.conllu'
        # If such a file doesn't exist, just use the original which is named
        # folder without UD_ + '.conllu'

    answer += avaa(file)

    os.chdir(rootfolder)

answer = answer.strip()

g = answer.split('\n\n') # merkkijonot
''')
    g = [w for w in g if w.strip()]
    h = [to_ordered_dict(w) for w in g]
    zero = []
    for sent in h:
        if possessive(sent, dict)['zero_marked']:
            zero.append(sent)
    

