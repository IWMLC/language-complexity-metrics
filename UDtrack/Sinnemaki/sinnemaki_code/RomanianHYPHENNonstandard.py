from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3].replace('HYPHEN', '-')



def possessive(conllu_item, returntype=list):
    """Will always return a dict, the returntype argument is a needless remnant of a previous phase of the project"""
    try:
        analyses = conllu_item['analyysit']
    except TypeError:
        print(conllu_item)
        return {'dep_marked':[], 'head_marked':[], 'double_marked':[], 'zero_marked':[], 'head_exist':[]}

    sent_id = conllu_item['sent_id']

    # Building dep_head_exist

    def find_head_index(analysis):
        head_str = analysis[6]
        head_i = int(head_str)-1
        return head_i

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []
    head_exist = [] # items are heads

    for a in analyses:
        # mostly pronouns
        # case 1
        if a[3] == 'PRON' and 'Poss=Yes' in a[5] and 'PronType=Prs' in a[5] and a[7] == 'det':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        # case 2
        elif a[3] == 'PRON' and 'Poss=Yes' in a[5] and 'PronType=Prs' in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)
        
        # case 3
        elif a[3] == 'PRON' and 'Case=Gen' in a[5] and 'PronType=Prs' in a[5] and 'Reflex=Yes' not in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        elif a[3] == 'PRON' and 'Case=Dat,Gen' in a[5] and 'PronType=Prs' in a[5] and 'Reflex=Yes' not in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)


        # nouns
        # case 1
        if a[2] == 'de' and a[3] == 'ADP' and 'Case=Acc' in a[5] and 'PronType=Prs' in a[5] and a[7] == 'case':
            dep_i = find_head_index(a)
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and 'Acc,Nom' in a[5] and a[7] == 'nmod':
                    head_i = find_head_index(a)
                    if head_i >= 0:
                        head = analyses[head_i]
                        if head[3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(a)
        # case 2
        elif a[2] == 'al' and a[3] == 'DET' and 'Poss=Yes' in a[5] and 'PronType=Art' in a[5] and a[7] == 'det':
            dep_i = find_head_index(a)
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and ('Case=Dat,Gen' in a[5] or 'Case=Gen' in a[5]) and a[7] == 'nmod':
                    head_i = find_head_index(a)
                    if head_i >= 0:
                        head = analyses[head_i]
                        if head[3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(a)
        # case 3
        elif a[3] in {'NOUN', 'PROPN'} and 'Case=Dat,Gen' in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)
        # case 4
        elif a[3] in {'NOUN', 'PROPN'} and 'Case=Gen' in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}



test = r'''# sent_id = train-3787
# text = Feriți-vă să nu cumva să se îngreuieze inimile voastre cu sațiul mîncării și bețiii și cu grijile ceștii lumi, și degrabă să vie zuoa aceaia.
# citation-part=LUCA 21.34
1	Feriți-	feri	VERB	Vmm-2p	Mood=Imp|Number=Plur|Person=2|VerbForm=Fin	0	root	_	ref=LUCA21.34|SpaceAfter=No
2	vă	tu	PRON	Pp2-pa--------w	Case=Acc|Number=Plur|Person=2|PronType=Prs|Strength=Weak	1	obj	_	ref=LUCA21.34
3	să	să	PART	Qs	PartType=Sub	5	mark	_	ref=LUCA21.34
4	nu	nu	ADV	Qz	Polarity=Neg	5	advmod	_	ref=LUCA21.34
5	cumva	cumva	ADV	Rg	_	1	ccomp:pmod	_	ref=LUCA21.34
6	să	să	PART	Qs	PartType=Sub	8	mark	_	ref=LUCA21.34
7	se	sine	PRON	Px3--a--------w	Case=Acc|Person=3|PronType=Prs|Strength=Weak	8	expl:pv	_	ref=LUCA21.34
8	îngreuieze	îngreuia	VERB	Vmsp3	Mood=Sub|Person=3|Tense=Pres|VerbForm=Fin	5	csubj	_	ref=LUCA21.34
9	inimile	inimă	NOUN	Ncfpry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Plur	8	nsubj	_	ref=LUCA21.34
10	voastre	tău	DET	Ds2fp-p	Gender=Fem|Number=Plur|Number[psor]=Plur|Person=2|PronType=Prs	9	det	_	ref=LUCA21.34
11	cu	cu	ADP	Spsa	AdpType=Prep|Case=Acc	12	case	_	ref=LUCA21.34
12	sațiul	sațiu	NOUN	Ncmsry	Case=Acc,Nom|Definite=Def|Gender=Masc|Number=Sing	8	obl	_	ref=LUCA21.34
13	mîncării	mâncare	NOUN	Ncfsoy	Case=Dat,Gen|Definite=Def|Gender=Fem|Number=Sing	12	nmod	_	ref=LUCA21.34
14	și	și	CCONJ	Ccssp	Polarity=Pos	15	cc	_	ref=LUCA21.34
15	bețiii	bețiii	NOUN	Ncmpry	Case=Acc,Nom|Definite=Def|Gender=Masc|Number=Plur	13	conj	_	ref=LUCA21.34
16	și	și	CCONJ	Ccssp	Polarity=Pos	18	cc	_	ref=LUCA21.34
17	cu	cu	ADP	Spsa	AdpType=Prep|Case=Acc	18	mark	_	ref=LUCA21.34
18	grijile	grijă	NOUN	Ncfpry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Plur	12	conj	_	ref=LUCA21.34
19	ceștii	acesta	DET	Dd3fso---e	Case=Dat,Gen|Gender=Fem|Number=Sing|Person=3|Position=Prenom|PronType=Dem	18	nmod	_	ref=LUCA21.34
20	lumi	lume	NOUN	Ncfson	Case=Dat,Gen|Definite=Ind|Gender=Fem|Number=Sing	19	nmod	_	ref=LUCA21.34|SpaceAfter=No
21	,	,	PUNCT	COMMA	_	25	punct	_	ref=LUCA21.34
22	și	și	CCONJ	Ccssp	Polarity=Pos	25	cc	_	ref=LUCA21.34
23	degrabă	degrabă	ADV	Rg	_	25	advmod:tmod	_	ref=LUCA21.34
24	să	să	PART	Qs	PartType=Sub	25	mark	_	ref=LUCA21.34
25	vie	veni	VERB	Vmsp3s	Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	8	conj	_	ref=LUCA21.34
26	zuoa	zi	NOUN	Ncfsry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Sing	25	nsubj	_	ref=LUCA21.34
27	aceaia	acela	DET	Dd3fsr	Case=Acc,Nom|Gender=Fem|Number=Sing|Person=3|PronType=Dem	26	det	_	ref=LUCA21.34|SpaceAfter=No
28	.	.	PUNCT	PERIOD	_	1	punct	_	ref=LUCA21.34'''

conllu_item = to_ordered_dict(test)
d = possessive(conllu_item, dict)

if __name__ == '__main__':
    if type(d) == dict:
        for item in d:
            print(item, d[item])
    else:
        for item in d:
            print(item)


def str2poss(s, returntype=list):
    conllu_item = to_ordered_dict(s)
    return possessive(conllu_item, returntype)

def str2bea(s, returntype=list):
    d = str2poss(s, returntype)
    if type(d) == dict:
        for item in d:
            print(item, d[item], len(d[item]))
    else:
        for item in d:
            print(item)


def strip_indent(s, i=1):
    c = []
    for j in s.splitlines():
        c.append(j[4*i:])
    return '\n'.join(c)

