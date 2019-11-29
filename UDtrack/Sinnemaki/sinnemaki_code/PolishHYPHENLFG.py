from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3].replace('HYPHEN', '-')

def possessive(conllu_item, returntype=list):
    """The return type is a dict, the "returntype" argument is a needless remnant of a previous phase of this project.
The point is to avoid crashing if an extra argument is given."""
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
    
    head_exist = []

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []

    for a in analyses:

        # pronouns
        if a[3] == 'PRON' and a[7] == 'nmod:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        if a[3] == 'DET' and 'Poss=Yes' in a[5] and 'PronType=Prs' in a[5] and 'Reflex=Yes' not in a[5] and a[7] == 'det':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        if a[3] == 'DET' and 'Poss=Yes' in a[5] and 'PronType=Prs' in a[5] and a[7] == 'nmod:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        # nouns

        if a[3] in {'NOUN', 'PROPN'} and 'Case=Gen' in a[5] and a[7] == 'nmod:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    if a[1].lower() == a[2].lower(): # if the dependent's word form is the same as the lemma, then it's a zero marked example
                        zero_marked.append(a)
                    else:
                        dep_marked.append(a)
            
    
    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = train-5759
# text = - Nasi przyjaciele wciąż nie mogą otrząsnąć się z szoku...
# converted_from_file = NKJP1M_1202000009_morph_70-p_morph_70.24-s-dis@1.xml
# genre = news
1	-	-	PUNCT	interp	PunctType=Dash	6	punct	6:punct	_
2	Nasi	nasz	DET	adj:pl:nom:m1:pos	Case=Nom|Gender=Masc|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs|SubGender=Masc1	3	det	3:det	_
3	przyjaciele	przyjaciel	NOUN	subst:pl:nom:m1	Case=Nom|Gender=Masc|Number=Plur|SubGender=Masc1	6	nsubj	6:nsubj|7:nsubj	_
4	wciąż	wciąż	ADV	adv	_	6	advmod	6:advmod	_
5	nie	nie	PART	qub	Polarity=Neg	6	advmod	6:advmod	_
6	mogą	móc	VERB	fin:pl:ter:imperf	Aspect=Imp|Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	0:root	_
7	otrząsnąć	otrząsnąć	VERB	inf:perf	Aspect=Perf|VerbForm=Inf|Voice=Act	6	xcomp	6:xcomp	_
8	się	się	PRON	qub	PronType=Prs|Reflex=Yes	7	expl:pv	7:expl:pv	_
9	z	z	ADP	prep:gen:nwok	AdpType=Prep|Variant=Short	10	case	10:case	Case=Gen
10	szoku	szok	NOUN	subst:sg:gen:m3	Case=Gen|Gender=Masc|Number=Sing|SubGender=Masc3	7	obl	7:obl:z	SpaceAfter=No
11	.	.	PUNCT	interp	PunctType=Peri	6	punct	6:punct	SpaceAfter=No
12	.	.	PUNCT	interp	PunctType=Peri	6	punct	6:punct	SpaceAfter=No
13	.	.	PUNCT	interp	PunctType=Peri	6	punct	6:punct	_'''

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
    

