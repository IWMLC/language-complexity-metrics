from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3].replace('HYPHEN', '-')



def possessive(conllu_item, returntype=list):
    """Will always return a dict, the returntype argument is a needless remnant of a previous phase of this project"""
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
        if a[2] == 'de' and a[3] == 'ADP' and 'Case=Acc' in a[5] and a[7] == 'case':
            dep_i = find_head_index(a)
            if dep_i >= 0:
                dep = analyses[dep_i] # THIS DEPENDENT CAN ALSO BE A NOUN
                if dep[3] in {'PRON', 'NOUN', 'PROPN'} and 'Acc,Nom' in a[5] and a[7] == 'nmod':
                    head_i = find_head_index(dep)
                    if head_i >= 0:
                        head = analyses[head_i]
                        if head[3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(dep)

        # case 2
        if a[3] == 'PRON' and ('Case=Dat,Gen' in a[5] or 'Case=Gen' in a[5]) and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)
        # cases 3 and 4
        if a[3] == 'PRON' and 'Poss=Yes' in a[5] and 'PronType=Prs' in a[5] and a[7] in {'det', 'nmod'}:
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        # nouns
        # case 2
        if a[2] == 'al' and a[3] == 'DET' and 'Poss=Yes' in a[5] and 'PronType=Prs' in a[5] and a[7] == 'det':
            dep_i = find_head_index(a)
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and ('Case=Dat,Gen' in a[5] or 'Case=Gen' in a[5]) and a[7] == 'nmod':
                    head_i = find_head_index(a)
                    if head_i >= 0:
                        head = analyses[head_i]
                        if head[3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(a)
                                      
        # cases 3 and 4
        if a[3] in {'NOUN', 'PROPN'} and ('Case=Dat,Gen' in a[5] or 'Case=Gen' in a[5]) and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                head = analyses[head_i]
                if head[3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}



test = r'''# newdoc id = 1984Orwell-b1-ttl
# sent_id = dev-1
# text = Într-o zi senină și friguroasă de aprilie, pe când ceasurile băteau ora treisprezece, Winston Smith, cu bărbia înfundată în piept pentru a scăpa de vântul care-l lua pe sus, se strecură iute prin ușile de sticlă ale Blocului Victoria, deși nu destul de repede pentru a împiedica un vârtej de praf și nisip să pătrundă o dată cu el.
1	Într-	întru	ADP	Spsay	AdpType=Prep|Case=Acc|Variant=Short	3	case	_	SpaceAfter=No
2	o	un	DET	Tifsr	Case=Acc,Nom|Gender=Fem|Number=Sing|PronType=Ind	3	det	_	_
3	zi	zi	NOUN	Ncfsrn	Case=Acc,Nom|Definite=Ind|Gender=Fem|Number=Sing	37	nmod:tmod	_	_
4	senină	senin	ADJ	Afpfsrn	Case=Acc,Nom|Definite=Ind|Degree=Pos|Gender=Fem|Number=Sing	3	amod	_	_
5	și	și	CCONJ	Crssp	Polarity=Pos	6	cc	_	_
6	friguroasă	friguros	ADJ	Afpfsrn	Case=Acc,Nom|Definite=Ind|Degree=Pos|Gender=Fem|Number=Sing	4	conj	_	_
7	de	de	ADP	Spsa	AdpType=Prep|Case=Acc	8	case	_	_
8	aprilie	aprilie	NOUN	Ncms-n	Definite=Ind|Gender=Masc|Number=Sing	3	nmod	_	SpaceAfter=No
9	,	,	PUNCT	COMMA	_	3	punct	_	_
10	pe	pe	ADP	Spsa	AdpType=Prep|Case=Acc	13	mark	_	_
11	când	când	ADV	Rw	PronType=Int,Rel	10	fixed	_	_
12	ceasurile	ceas	NOUN	Ncfpry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Plur	13	nsubj	_	_
13	băteau	bate	VERB	Vmii3p	Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin	37	advcl:tcl	_	_
14	ora	oră	NOUN	Ncfsry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Sing	13	obj	_	_
15	treisprezece	treisprezece	NUM	Mc-p-l	Number=Plur|NumForm=Word|NumType=Card	14	nummod	_	SpaceAfter=No
16	,	,	PUNCT	COMMA	_	13	punct	_	_
17	Winston	Winston	PROPN	Np	_	37	nsubj	_	_
18	Smith	Smith	PROPN	Np	_	17	flat	_	SpaceAfter=No
19	,	,	PUNCT	COMMA	_	21	punct	_	_
20	cu	cu	ADP	Spsa	AdpType=Prep|Case=Acc	21	case	_	_
21	bărbia	bărbie	NOUN	Ncfsry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Sing	37	obl	_	_
22	înfundată	înfunda	VERB	Vmp--sf	Gender=Fem|Number=Sing|VerbForm=Part	21	amod	_	_
23	în	în	ADP	Spsa	AdpType=Prep|Case=Acc	24	case	_	_
24	piept	piept	NOUN	Ncms-n	Definite=Ind|Gender=Masc|Number=Sing	22	obl	_	_
25	pentru	pentru	ADP	Spsa	AdpType=Prep|Case=Acc	27	mark	_	_
26	a	a	PART	Qn	PartType=Inf	27	mark	_	_
27	scăpa	scăpa	VERB	Vmnp	Tense=Pres|VerbForm=Inf	22	obl	_	_
28	de	de	ADP	Spsa	AdpType=Prep|Case=Acc	29	case	_	_
29	vântul	vânt	NOUN	Ncmsry	Case=Acc,Nom|Definite=Def|Gender=Masc|Number=Sing	27	nmod:pmod	_	_
30	care	care	PRON	Pw3--r	Case=Acc,Nom|Person=3|PronType=Int,Rel	32	nsubj	_	SpaceAfter=No
31	-l	el	PRON	Pp3msa--y-----w	Case=Acc|Gender=Masc|Number=Sing|Person=3|PronType=Prs|Strength=Weak|Variant=Short	32	obj	_	_
32	lua	lua	VERB	Vmii3s	Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin	29	acl	_	_
33	pe	pe	ADP	Spsa	AdpType=Prep|Case=Acc	34	case	_	_
34	sus	sus	ADV	Rgp	Degree=Pos	32	advmod	_	SpaceAfter=No
35	,	,	PUNCT	COMMA	_	21	punct	_	_
36	se	sine	PRON	Px3--a--------w	Case=Acc|Person=3|PronType=Prs|Reflex=Yes|Strength=Weak	37	expl:pv	_	_
37	strecură	strecura	VERB	Vmis3s	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	0	root	_	_
38	iute	iute	ADV	Rgp	Degree=Pos	37	advmod	_	_
39	prin	prin	ADP	Spsa	AdpType=Prep|Case=Acc	40	case	_	_
40	ușile	ușă	NOUN	Ncfpry	Case=Acc,Nom|Definite=Def|Gender=Fem|Number=Plur	37	obl	_	_
41	de	de	ADP	Spsa	AdpType=Prep|Case=Acc	42	case	_	_
42	sticlă	sticlă	NOUN	Ncfsrn	Case=Acc,Nom|Definite=Ind|Gender=Fem|Number=Sing	40	nmod	_	_
43	ale	al	DET	Tsfp	Gender=Fem|Number=Plur|Poss=Yes|PronType=Prs	44	det	_	_
44	Blocului	bloc	NOUN	Ncmsoy	Case=Dat,Gen|Definite=Def|Gender=Masc|Number=Sing	40	nmod	_	_
45	Victoria	Victoria	PROPN	Np	_	44	nmod	_	SpaceAfter=No
46	,	,	PUNCT	COMMA	_	51	punct	_	_
47	deși	deși	SCONJ	Csssp	Polarity=Pos	51	mark	_	_
48	nu	nu	PART	Qz	Polarity=Neg	51	advmod	_	_
49	destul	destul	ADV	Rgp	Degree=Pos	51	advmod	_	_
50	de	de	ADP	Spsa	AdpType=Prep|Case=Acc	49	case	_	_
51	repede	repede	ADV	Rgp	Degree=Pos	37	advcl	_	_
52	pentru	pentru	ADP	Spsa	AdpType=Prep|Case=Acc	54	mark	_	_
53	a	a	PART	Qn	PartType=Inf	54	mark	_	_
54	împiedica	împiedica	VERB	Vmnp	Tense=Pres|VerbForm=Inf	51	advcl	_	_
55	un	un	DET	Timsr	Case=Acc,Nom|Gender=Masc|Number=Sing|PronType=Ind	56	det	_	_
56	vârtej	vârtej	NOUN	Ncms-n	Definite=Ind|Gender=Masc|Number=Sing	54	iobj	_	_
57	de	de	ADP	Spsa	AdpType=Prep|Case=Acc	58	case	_	_
58	praf	praf	NOUN	Ncms-n	Definite=Ind|Gender=Masc|Number=Sing	56	nmod	_	_
59	și	și	CCONJ	Crssp	Polarity=Pos	60	cc	_	_
60	nisip	nisip	NOUN	Ncms-n	Definite=Ind|Gender=Masc|Number=Sing	58	conj	_	_
61	să	să	PART	Qs	Mood=Sub	62	mark	_	_
62	pătrundă	pătrunde	VERB	Vmsp3	Mood=Sub|Person=3|Tense=Pres|VerbForm=Fin	54	ccomp	_	_
63	o	un	DET	Tifsr	Case=Acc,Nom|Gender=Fem|Number=Sing|PronType=Ind	62	advmod	_	_
64	dată	dată	NOUN	Ncfsrn	Case=Acc,Nom|Definite=Ind|Gender=Fem|Number=Sing	63	goeswith	_	_
65	cu	cu	ADP	Spsa	AdpType=Prep|Case=Acc	66	case	_	_
66	el	el	PRON	Pp3msr--------s	Case=Acc,Nom|Gender=Masc|Number=Sing|Person=3|PronType=Prs|Strength=Strong	62	obl	_	SpaceAfter=No
67	.	.	PUNCT	PERIOD	_	37	punct	_	_'''

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

