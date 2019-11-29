This is the readme file of the two scripts that have to be run in sequence in order to reproduce the submitted results. 

1)ling_monitoring.py

# `LingMonitoring` - Linguistic Features extraction

This contains scripts to extract linguistic features from previously parsed text. The features can be extracted both from single sentences and from whole documents (or collections of documents). The scripts was implemented to run on all datasets annotated with the Universal Dependencies annotation schema (https://universaldependencies.org/).

## Requirements
- Requires Python 3.x

## Type of input
- Text
 * The Linguistic Monitoring works on files containing sentences parsed in CoNLL-U format. More information about this format can be found in the [Universal Dependencies](https://universaldependencies.org/) page.


## Usage

To run use:

 `python ling_monitoring.py [-p PATH] [-t TYPE]`

* optional arguments

 `-h, --help` shows this help message and exit

 `-p YOUR_PATH, --path YOUR_PATH` specifies the path of the directory that contains the file or the files you want to analyse or specifies the single file you want to analyse

 `-t {0, 1}, -type {0, 1}` specify if you want to extract features from single sentences [0] or from a document containg one or more sentences [1]. 

To reproduce the output we submitted, it is required to run the option [0].

**WARNING** 
Note that before running `ling_monitoring.py` on treebanks containing Enhanced Depedency representations, you have to clean data removing all IDs corresponding to `enhanced' tokens. To do this, we provide a script named cleanConllU.py`.
## Usage
`python cleanConllU.py *namefile.conllu*
## Output
*namefile_cleaned.conllu*



## Output

For each input file, the output of the analysis is stored in a directory **output_results/** automatically created and it is named *namefile_sent.out* (for sentence analysis) or *namefile_doc.out* (for document analysis). The output contains for each sentence or document the list of extracted linguistic features separated by a tab. Es.

>>> namefile_sentence-id \t feature_name_1 \t feature_name_2 \t feature_name_3 ...
>>> namefile \t feature_name_1 \t feature_name_2 \t feature_name_3 ...

For sentence analysis, the output file will contain a line for each sentence contained in the input file.
For document analysis, the output file will contain a single line with the value of the extracted features.

2) average_scale.py

This is the script allowing
- to compute the average values of all extracted features from each sentence of an input file;
- to scale the average value of each feature with respect to the maximum value of the relative range.

## Requirements
- Requires Python 

## Type of input
- csv file in the directory **output_results**

## Usage

To run use:

`python average_scale.py output_results`

## Output

The script automatically produces a file named `italianlp-output.csv' containing for each input file, the average value of each feature scaled with respect to the maximum value of the relative range. Es.

>>> filename \t	feature_name_1 \t feature_name_2 \t feature_name_3 ...
Indonesian-GSD.conllu_sent.out	0.8555824037374429	1.0	0.9773736413384605	...	
Afrikaans-AfriBooms.conllu_sent.out	1.0	0.9150619469470934	1.0		...
...

The example reports the scaled average values of a subset of features extracted from the Indonesian and Afrikaans UDT. For instance, the value 1.0 means that Afrikaans has the maximum value for `feature_name_1'.

