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

    dep_head_exist = [] # items are dependents
    head_exist = []

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []

    for a in analyses:
        # a is DEPENDENT
        head_i = find_head_index(a)
        if head_i >= 0: # head must exist
            if a[3] in {'PRON', 'NOUN', 'PROPN'} and a[7] == 'det:poss' and analyses[head_i][3] in {'NOUN', 'PROPN'}:
                dep_marked.append(a) # Korean-GSD
            #elif a[2].endswith('의') and a[3] in {'PRON', 'NOUN', 'PROPN'} and a[7] == 'nmod' and analyses[head_i][3] in {'NOUN', 'PROPN'}:
                #dep_marked.append(a) # Korean-Kaist
    
    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = dev-s3
# text = 해당 질량은 항성의 구성 원소에 따라 태양의 1.2배에서 1.46배로 약간 차이가 난다.
1	해당	해당	NOUN	NNG	_	12	nsubj	_	_
2	질량은	질량+은	NOUN	NNG+JX	_	1	flat	_	_
3	항성의	항성+의	NOUN	NNG+JKG	_	4	det:poss	_	_
4	구성	구성	NOUN	NNG	_	6	advmod	_	_
5	원소에	원소+에	ADV	NNG+JKB	_	4	flat	_	_
6	따라	따르+아	VERB	VV+EC	_	12	advcl	_	_
7	태양의	태양+의	NOUN	NNG+JKG	_	9	det:poss	_	_
8	1.2배에서	1.2+배+에서	ADV	SN+NNG+JKB	_	9	advmod	_	_
9	1.46배로	1.46+배+로	ADV	SN+NNG+JKB	_	12	obl	_	_
10	약간	약간	ADV	MAG	_	12	advmod	_	_
11	차이가	차이+가	NOUN	NNG+JKS	_	12	nsubj	_	_
12	난다	나+ㄴ다	VERB	VV+EF	_	0	root	_	SpaceAfter=No
13	.	.	PUNCT	SF	_	12	punct	_	_'''

conllu_item = to_ordered_dict(test)
d = possessive(conllu_item, dict)

if __name__ == '__main__':
    if type(d) == dict:
        for item in d:
            print(item, d[item], len(d[item]))
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
    

