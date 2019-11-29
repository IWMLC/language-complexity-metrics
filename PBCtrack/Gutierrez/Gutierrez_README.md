# IWMLC 2019

Script for calculating the TTR and the entropy rate of a corpus.

This program runs in python 3. The program uses the next libraries:

* Standard pyhton libraries (numpy, collections, itertools, random, re)
* nltk (Natural Language Toolkit) https://www.nltk.org/ 

## Basic Usage

To run the script, execute the following command:<br/>

	``python3 main.py --input corpora --output results/results.csv``

### Input/Output directories
The script requires the following directories to be specified:

* input : input directory of data (Default is corpora).
* output : output directory (Default is results/results.csv)

The output csv will contain: filename, H-ngram, TTR


##### Parameters for the entropy rate of the neural probabilistic language model:

* n : the size of n-grams. Default is 3
* iter : number of iterations to train the neural network. Default is 50
* subsample_siz : Number of examples for epoch in SGD. Default is 300
* emb_dim : Number of dimensions in embedding vectors. Default is 300
* hid_dim : Number of dimensions in hidden layer. Default is 100

To run the model with different parameters, execute the program as in the following example:<br/>

	``python3 main.py --input corpora --output results/results.csv --n 1 --iter 100``

### Remarks
The combined rankings measures (TTR+Hngram) are not included in this script, since they were directly obtained using spreadsheets.
 
