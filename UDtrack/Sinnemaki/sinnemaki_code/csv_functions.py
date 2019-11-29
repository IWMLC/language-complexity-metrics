import csv
from conllu_reader import avaa

def csv2list(source_name):
    with open(source_name, encoding='utf-8') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        return list(read_csv)    

def list2csv(data, output_name):
    """Write csv file from list of lists of strings/numbers."""
    with open(output_name, 'wt', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

def readbytes(d):
    with open(d, 'rb') as k:
        return k.read()

readstring = avaa

def writebytes(d, output_name):
    with open(output_name, 'wb') as k:
        k.write(d)

def writestring(d, output_name):
    with open(output_name, 'wt', encoding='utf-8') as k:
        print(d, file=k, end='')

def read_table(source_name):
    """Read tab separated table."""
    return [line.split('\t') for line in avaa(source_name).strip('\n').splitlines()]

def write_table(d, output_name):
    with open(output_name, 'wt', encoding='utf-8') as k:
        for line in d:
            print('\t'.join([str(i) for i in line]), file=k)

def tabsep2csv(source_name, output_name, first_n_columns=None):
    """Convert tab separated file to csv. Optionally exclude last columns from conversion, taking in only columns up to parameter first_n_columns."""
    if first_n_columns is None:
        list2csv(read_table(source_name), output_name)
    else:
        table = [a[:first_n_columns] for a in read_table(source_name)]
        list2csv(table, output_name)
