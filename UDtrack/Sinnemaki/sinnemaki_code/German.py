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

    for a in analyses: # a could be the dependent or the adposition (equivalent of 'of'),
        #which is the reason that the initial variable name is nothing more descriptive than that.
        #The name of the head variable ("head" or "dep") is supposed to be more descriptive:
        #if it's "head", then "a" is a dependent, if it's "dep", then "a" is the adposition.
        # pronouns
        if a[3] == 'DET' and 'Poss=Yes' in a[5] and a[7] == 'det:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        elif a[3] == 'PRON' and 'Poss=Yes' in a[5] and a[7] == 'det:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        elif a[3] == 'DET' and 'PronType=Prs' in a[5] and a[7] == 'det:poss':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        # nouns  
        elif a[2] == 'von' and a[3] == 'ADP' and a[7] == 'nmod':
            dep_i = find_head_index(a) # von structures
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and 'Case=Dat' in dep[5] and dep[7] == 'nmod':
                    head_i = find_head_index(a)
                    if head_i >= 0:
                        head = analyses[head_i]
                        if head[3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(dep)

        elif a[3] == 'DET' and 'Case=Gen' in a[5] and 'PronType=Art' in a[5] and a[7] == 'det':
            dep_i = find_head_index(a) # genitive structures
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and 'Case=Gen' in dep[5] and dep[7] == 'nmod':
                    head_i = find_head_index(a)
                    if head_i >= 0:
                        head = analyses[head_i]
                        if head[3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(dep)

    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = dev-s15
# text = Wir hatten wunderschöne Spaziergänge und die Städte der Region mit Ihren Gründerzeithäusern sind sehenswert.
1	Wir	wir	PRON	PPER	Case=Nom|Number=Plur|Person=1|PronType=Prs	2	nsubj	_	_
2	hatten	haben	VERB	VAFIN	Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin	0	root	_	_
3	wunderschöne	wunderschön	ADJ	ADJA	Case=Acc|Gender=Masc|Number=Plur	4	amod	_	_
4	Spaziergänge	Spaziergang	NOUN	NN	Case=Acc|Gender=Masc|Number=Plur	2	obj	_	_
5	und	und	CCONJ	KON	_	14	cc	_	_
6	die	der	DET	ART	Case=Acc|Definite=Def|Gender=Fem|Number=Plur|PronType=Art	7	det	_	_
7	Städte	Stadt	NOUN	NN	Case=Acc|Gender=Fem|Number=Plur	14	nsubj	_	_
8	der	der	DET	ART	Case=Gen|Definite=Def|Gender=Fem|Number=Sing|PronType=Art	9	det	_	_
9	Region	Region	NOUN	NN	Case=Gen|Gender=Fem|Number=Sing	7	nmod	_	_
10	mit	mit	ADP	APPR	_	12	case	_	_
11	Ihren	ihr	PRON	PPOSAT	Case=Dat|Gender=Neut|Number=Plur|Poss=Yes	12	det:poss	_	_
12	Gründerzeithäusern	Gründerzeithaus	NOUN	NN	Case=Dat|Gender=Neut|Number=Plur	7	nmod	_	_
13	sind	sein	AUX	VAFIN	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin	14	cop	_	_
14	sehenswert	sehenswert	ADJ	ADJD	_	2	conj	_	SpaceAfter=No
15	.	.	PUNCT	$.	_	2	punct	_	_'''

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
