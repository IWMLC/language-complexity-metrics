from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

personal_pronouns = {'anh', 'ấy', 'chúng', 'chúng ta', 'chúng tôi', 'hắn',
                     'họ', 'mày', 'mình', 'nó', 'ông', 'ta', 'tôi', 'tui', 'y'}

def possessive(conllu_item, returntype=list):
    """The returntype argument is unused, the function returns a dict. It's a remnant of a previous phase of the project,
currently there only to avoid crashing if an extra argument is given."""
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
    double_marked = []
    head_marked = []
    zero_marked = []
    head_exist = []

    for a in analyses: # Check each word in sentence if it's a dependent or an adposition (meaning: 'of') of a possessive NP.
        if a[2] in personal_pronouns and a[3] == 'PROPN' and a[7] == 'det':
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    for word in analyses:
                        if word[2] == 'của' and word[6] == a[0] and word[3] == 'ADP' and word[7] == 'case':
                            dep_marked.append(a)
                            break
                    else:
                        zero_marked.append(a)
        elif a[2] == 'của' and a[3] == 'ADP' and a[7] == 'case': # This is the particle/adpositional case.
            dep_i = find_head_index(a)
            if dep_i > 0:
                dependent = analyses[dep_i]
                if dependent[3] in {'NOUN', 'PROPN'} and dependent[7] == 'nmod':
                    head_i = find_head_index(dependent)
                    if head_i >= 0:
                        if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(dependent)

    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = dev-s1
# text = Hay một người lính hải quân Pháp đã rải truyền đơn cho người dân nước Pháp cùng chống lại cuộc chiến phi nghĩa của quân đội Pháp tại VN.
1	Hay	Hay	CCONJ	C	_	8	cc	_	_
2	một	một	NUM	M	NumType=Card	4	nummod	_	_
3	người	người	NOUN	Nc	_	4	compound	_	_
4	lính	lính	NOUN	N	_	8	nsubj	_	_
5	hải quân	hải quân	NOUN	N	_	4	compound	_	_
6	Pháp	Pháp	NOUN	Np	_	5	compound	_	_
7	đã	đã	X	R	_	8	advmod	_	_
8	rải	rải	VERB	V	_	0	root	_	_
9	truyền đơn	truyền đơn	NOUN	N	_	8	obj	_	_
10	cho	cho	ADP	E	_	12	case	_	_
11	người	người	NOUN	Nc	_	12	compound	_	_
12	dân	dân	NOUN	N	_	8	obl	_	_
13	nước	nước	NOUN	N	_	12	compound	_	_
14	Pháp	Pháp	NOUN	Np	_	13	compound	_	_
15	cùng	cùng	ADJ	A	_	8	xcomp	_	_
16	chống	chống	VERB	V	_	15	xcomp	_	_
17	lại	lại	X	R	_	16	advmod	_	_
18	cuộc chiến	cuộc chiến	NOUN	N	_	16	obj	_	_
19	phi nghĩa	phi nghĩa	ADJ	A	_	18	amod	_	_
20	của	của	ADP	E	_	21	case	_	_
21	quân đội	quân đội	NOUN	N	_	18	nmod	_	_
22	Pháp	Pháp	NOUN	Np	_	21	compound	_	_
23	tại	tại	ADP	E	_	24	case	_	_
24	VN	VN	NOUN	Ny	_	21	nmod	_	SpaceAfter=No
25	.	.	PUNCT	.	_	8	punct	_	_'''

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

