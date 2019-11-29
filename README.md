## language-complexity-metrics
Data, descriptions and code for metrics presented at the Interactive Workshop on Measuring Language Complexity

This repository comprises a collection of metrics of language complexity which were presented as part of the *Interactive Workshop on Measuring Language Complexity* ([IWMLC](http://christianbentz.de/MLC2019_index.html)) taking place at the *Freiburg Institute for Advanced Studies* in September 2019. 

### The workshop 

The workshop brought together researchers from cross-language typology and language evolution, psycholinguistics, first and second language acquisition, and computational linguistics, who are interested in measures of language complexity. 

Language complexity is a very popular topic internationally which has been hotly debated in the past decade and continues to fascinate researchers from diverse areas of linguistics and beyond. The early sociolinguistic-typological complexity debate centered around the question of whether, overall, all languages were of equal complexity or not. In the meantime, plenty of empirical evidence has shown that languages and language varieties can and do differ in their complexity. Measures of language complexity are as abundant and diverse as the research that has produced them. However, no universally accepted and applicable metric has so been found. 

Thus, the workshop aimed at evaluating and comparing different measures of language complexity by means of a shared task. 

### Research objectives

* How do different complexity metrics correlate across parallel and non-parallel corpora, and other types of data?

* How well do different complexity metrics deal with different language types, i.e. are some language types/families easier or more consistently measurable than others?
    
* How well do measures within each domain correlate? Do morphological complexity measures show better agreement than syntactic complexity measures?
   
* How robust are trade-offs, such as between morphology and syntax, across different measures and corpora?
   
* How do corpus-based complexity metrics correlate with the feature-based complexity information available in The World Atlas of Language Structures (WALS)?

### Shared task

The workshop participants applied their own measure(s) of language complexity to two common datasets:

* A sample of the Parallel Bible Corpus (PBC), a parallel text database. The sample comprises 49  typologically diverse languages selected on the basis of typological information from [*The World Atlas of Language Structures database*](https://wals.info/).

* A subset of the [Universal Dependencies](http://universaldependencies.org/) (UD) corpora v2.3 , a non-parallel annotated text database. The selected files of the UD cover 44 distinct languages.

The measures target language complexity at various linguistic levels, specifically, morphology, syntax, and the lexicon, or assess complexity in terms of information density. 

All participants submitted a .csv spreadsheet containing the results per language, and a brief description of the complexity metric(s) applied. In many cases, the code which was used to implement the measurements and instructions for running the code are included. 

### Folder structure

The repository contains two main directories:

#### PBCtrack 

PBCtrack contains all shared task data using the Parallel Bible Corpus. It specifically comprises the following subdirectories labelled after the participants’ surnames.
* Gutierrez (code included)
* Oh (code included)

#### UDtrack

UDtrack contains all shared task data using the Universal Dependencies corpora. It specifically comprises the following subdirectories labelled after the participants’ surnames.

* Brunato_venturi 
* Coltekin_rama (code available on https://github.com/coltekin/mlc2018)
* Semenuks (code included)
* Sinnemaki (code included)
* Sozinova_etal (code included, see also https://github.com/avonizos)

