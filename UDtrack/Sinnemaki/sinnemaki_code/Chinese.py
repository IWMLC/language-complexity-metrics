from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

def possessive(conllu_item, returntype=list):
    """Return type is always dict, the argument is a remnant of an undecided phase of the project."""
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

    for a in analyses:
        # this is what the PronTags file said, probably not exactly as intended
        if a[3] == 'PRON' and 'Person=' in a[5] and a[7] == 'det':
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    zero_marked.append(a)
        elif a[3] == 'PRON' and 'Person=' in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)


        elif a[3] == 'PART' and 'Case=Gen' in a[5] and a[7] == 'case:dec':
            dep_i = find_head_index(a)
            if dep_i >= 0:
                dep = analyses[dep_i]
                if dep[3] in {'NOUN', 'PROPN'} and dep[7] == 'det':
                    head_i = find_head_index(dep)
                    if head_i >= 0:
                        if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                            dep_marked.append(dep)


    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}



test = r'''# sent_id = dev-s2
# text = 大多數的加長型禮車則是租車公司的財產.
1	大	大	ADV	RB	_	2	advmod	_	SpaceAfter=No
2	多數	多數	ADJ	JJ	_	6	det	_	SpaceAfter=No
3	的	的	PART	DEC	Case=Gen	2	case:dec	_	SpaceAfter=No
4	加長	加長	VERB	VV	_	5	case:suff	_	SpaceAfter=No
5	型	型	PART	SFN	_	6	nmod	_	SpaceAfter=No
6	禮車	禮車	NOUN	NN	_	11	nsubj	_	SpaceAfter=No
7	則是	則是	AUX	VC	_	11	cop	_	SpaceAfter=No
8	租車	租車	NOUN	NN	_	9	nmod	_	SpaceAfter=No
9	公司	公司	NOUN	NN	_	11	det	_	SpaceAfter=No
10	的	的	PART	DEC	Case=Gen	9	case:dec	_	SpaceAfter=No
11	財產	財產	NOUN	NN	_	0	root	_	SpaceAfter=No
12	.	.	PUNCT	.	_	11	punct	_	SpaceAfter=No'''

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

