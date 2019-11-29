from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

def possessive(conllu_item, returntype=list):
    """The returntype argument is unused, the function returns a dict. It's a remnant of a previous phase of the project,
currently there only to avoid crashing if an extra argument is given."""
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

    def this_is_head_of(analysis):
        nonlocal analyses
        answer = []
        for a in analyses:
            if a[6] == analysis[0]:
                answer.append(a)
        return answer
    

    #dep_head_exist = [] # items are dependents
    head_exist = [] # items are heads

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []

    def genitive(analysis):
        return 'Case=Gen' in a[5] or 'Poss=Yes' in a[5] or 'GEN' in a[4].replace('-', '|').split('|')

    for a in analyses:
        # a is DEPENDENT
        head_i = find_head_index(a)
        if head_i >= 0: # head must exist

            #Genitive structures
            if (a[3] in {'NOUN', 'PROPN', 'PRON'} and a[7] == 'nmod:poss'):# or (a[3] == 'DET' and a[7] == 'det'):
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    a_is_genitive = genitive(a)
                    
                    if a_is_genitive:# and 'psor' not in analyses[head_i][5]: (there are no "psor"s in either Swedish file)
                        if a[3] in {'NOUN', 'PROPN'} and a[1].lower() == a[2].lower():
                            tiho = this_is_head_of(a)
                            if not tiho:
                                zero_marked.append(a)
                            elif all(b[7] == 'flat' and b[1].lower() == b[2].lower() for b in tiho):
                                zero_marked.append(a) # sent 4043 "New yorks" leads here, but it has a mistake in analysis,
                                # the lemma of "yorks" should be "york" not "yorks".
                            elif any(b[7] == 'flat' and b[1].lower() != b[2].lower() for b in tiho):
                                dep_marked.append(a)
                        else:
                            dep_marked.append(a)
                
                    elif 'Case=Gen' not in a[5]:# and 'psor' not in analyses[head_i][5]:
                        tiho = this_is_head_of(a)
                        for b in tiho:
                            #William Wilsons
                            if 'flat' in b[7] and 'Case=Gen' in b[5]:
                                dep_marked.append(a)
                                break
                            #släkt- och generationsbandens
                            elif '-|-' in a[4] and 'Case=Gen' in b[5]:
                                dep_marked.append(a)
                                break
                        else:
                            zero_marked.append(a)

            # av structures
            elif a[2] == 'av' and a[3] == 'ADP' and a[7] == 'case':
                dep_i = find_head_index(a)
                if dep_i >= 0:
                    dep = analyses[dep_i]
                    if dep[3] in {'NOUN', 'PROPN', 'PRON'} and dep[7] == 'nmod':
                        head_i = find_head_index(dep)
                        if head_i >= 0:
                            head = analyses[head_i]
                            if head[3] in {'NOUN', 'PROPN'}:
                                dep_marked.append(dep)

    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = 2753
# text = Den aktuella Windows NT-användaren måste vara medlem i datorns administratörsgrupp.
1	Den	den	DET	SG-DEF	Definite=Def|Gender=Com|Number=Sing|PronType=Art	4	det	_	_
2	aktuella	aktuell	ADJ	POS-DEF	Case=Nom|Definite=Def|Degree=Pos|Number=Sing	4	amod	_	_
3	Windows	Windows	PROPN	SG-NOM	Case=Nom	4	nmod	_	_
4	NT-användaren	NT-användare	NOUN	SG-DEF-NOM	Case=Nom|Definite=Def|Gender=Com|Number=Sing	7	nsubj	_	_
5	måste	måste	AUX	AUX	Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Act	7	aux	_	_
6	vara	vara	AUX	INF-ACT	VerbForm=Inf|Voice=Act	7	cop	_	_
7	medlem	medlem	NOUN	SG-IND-NOM	Case=Nom|Definite=Ind|Gender=Com|Number=Sing	0	root	_	_
8	i	i	ADP	_	_	10	case	_	_
9	datorns	dator	NOUN	SG-DEF-GEN	Case=Gen|Definite=Def|Gender=Com|Number=Sing	10	nmod:poss	_	_
10	administratörsgrupp	administratörsgrupp	NOUN	SG-IND-NOM	Case=Nom|Definite=Ind|Gender=Com|Number=Sing	7	nmod	_	SpaceAfter=No
11	.	.	PUNCT	Period	_	7	punct	_	_'''

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
        

    

