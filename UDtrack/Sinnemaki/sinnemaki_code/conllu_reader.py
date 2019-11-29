from collections import OrderedDict

def avaa(x): # open file. Named in Finnish to not confuse with built-in open
    with open(x, 'rt', encoding='utf-8') as k:
        b = k.read()
        return b[b.startswith('\ufeff'):] # remove initial '\ufeff' if present


def to_ordered_dict(item):
    try:
        answer = OrderedDict()
        lines = item.splitlines()
        for n, line in enumerate(lines):
            if line[0].isdigit(): # stop when actual word found
                break
            if line.startswith('#'):
                cline = line[1:].split('=')
                answer[cline[0].strip()] = '='.join(cline[1:]).strip()
            else:
                cline = line.split('=')
                answer[cline[0].strip()] = '='.join(cline[1:]).strip()
        final_list = []
        nan_start = []


        while n < len(lines): # n is remembered after the break of the for loop
            linesplit = lines[n].split('\t')

            if linesplit[0].isdigit():
                final_list.append(linesplit)
            else:
                nan_start.append(linesplit)
            n += 1

        answer['analyysit'] = final_list # analyysit = analyses /əˈnæl.ɪ.siːz/ in Finnish
        # just in case a line starting with "# analyses = " happened to appear in the source
        answer['ei-numeroalkuiset'] = nan_start # Rows whose first element was not a number, e.g. "1-2" (contractions)

        return answer
    except UnboundLocalError:
        return None # if, for instance, not a valid string

def to_str(ordered_dict):
    answer = []
    for k, v in ordered_dict.items():
        if k == 'analyysit':
            for line in v:
                answer.append('\t'.join(line))
        else:
            answer.append('# {} = {}'.format(k, v))
    return '\n'.join(answer)

def equal_content(ordered_dict_1, ordered_dict_2):
    """Compare if two OrderedDicts are equal when order is ignored"""
    return dict(ordered_dict_1) == dict(ordered_dict_2)

def str2list(s):
    """Convert a conllu string (content of a file) into list of OrderedDicts"""
    answer = []
    for item in s.split('\n\n'):
        analysis = to_ordered_dict(item)
        if analysis and 'sent_id' in analysis and 'text' in analysis and 'analyysit' in analysis:
            # make sure this is a real conllu analysis and not a result of a broken source
            answer.append(analysis)
    return answer

def path2list(s):
    """Convert a path to a conllu file into a list of OrderedDicts"""
    return str2list(avaa(s))

