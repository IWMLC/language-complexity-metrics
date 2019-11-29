from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

def possessive(conllu_item, returntype=list):
    """Will always return a dict, the argument is needless, but a remnant of a previous phase of the project"""
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
    head_exist = [] # items are heads

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []

    for a in analyses:
        # a is DEPENDENT
        head_i = find_head_index(a)
        if head_i >= 0: # head must exist
            # There is no 'det:poss' tag in Korean-GSD so this wouldn't mess up the results,
            # it would just make the script a little slower.
            #if a[3] in {'PRON', 'NOUN', 'PROPN'} and a[7] == 'det:poss' and analyses[head_i][3] in {'NOUN', 'PROPN'}:
                #dep_marked.append(a) # Korean-GSD
            
            if a[2].endswith('의') and a[3] in {'PRON', 'NOUN', 'PROPN'} and a[7] == 'nmod' and analyses[head_i][3] in {'NOUN', 'PROPN'}:
                dep_marked.append(a) # Korean-Kaist
    
    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}



test = r'''# sent_id = M2TA_069-s29
# text = 옛 서울의 아름답던 기와집들은 모두 불에 타 없어지고 초가집으로 바뀔 수밖에 없었습니다 .
1	옛	옛	ADJ	mma	_	2	amod	_	_
2	서울의	서울+의	PROPN	nq+jcm	_	4	nmod	_	_
3	아름답던	아름답+던	ADJ	paa+etm	_	4	amod	_	_
4	기와집들은	기와집+들+은	NOUN	ncn+xsn+jxt	_	10	dislocated	_	_
5	모두	모두	ADV	mag	_	7	advmod	_	_
6	불에	불+에	ADV	ncn+jca	_	7	obl	_	_
7	타	타+아	SCONJ	pvg+ecs	_	0	root	_	_
8	없어지고	없+어+지+고	CCONJ	paa+ecx+px+ecc	_	7	conj	_	_
9	초가집으로	초가집+으로	ADV	ncn+jca	_	10	advcl	_	_
10	바뀔	바뀌+ㄹ	VERB	pvg+etm	_	7	conj	_	_
11	수밖에	수+밖에	ADV	nbn+jxc	_	10	aux	_	_
12	없었습니다	없+었+습니다	ADJ	paa+ep+ef	_	11	fixed	_	_
13	.	.	PUNCT	sf	_	11	punct	_	_'''

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
    

