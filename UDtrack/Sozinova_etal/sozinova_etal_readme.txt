0. The program is written using Python 3 and was tested on MacOS Mojave, Windows 10 and Linux Ubuntu 14.04.5.

1. The program requires an external package Morfessor.
Please install it before running the program by using this command:

pip install morfessor==2.0.4

In case of permission error run: 

sudo pip install morfessor==2.0.4

2. The program takes 3 input parameters:

-p  path to the folder "UDtrack"
-f  path to the CSV file, where the results are written (in ud_template format)
-e  optional parameter; set to True, if you want to write an additional CSV table with extended results, which includes:
language name, filename, number of tokens, number of word types in the raw text, number of word types in the lemmatized text, entropy of the raw text (H_raw), entropy of the lemmatized text (H_lemmas), entropy of the segmented text (H_segments), difference between H_raw and H_lemmas (SBS_INF in ud_template format), difference between H_lemmas and H_segments (SBS_DER in ud_template format)

The CSV file is named 'extended_results.csv' and is situated in the same folder as the program count_entropy.py

Examples of use:

python count_entropy.py -p UDtrack -f sozinova_etal.csv (outputs only results in ud_template format)
python count_entropy.py -p UDtrack -f sozinova_etal.csv -e True (outputs both results in ud_template format and the extended results)

If you have different versions of Python installed on your machine, make sure that you run the code under Python 3 (using python3 command instead of python). The program does not work in Python 2.

Running time takes several hours, because of the morphological segmentation.
The process of segmentation is printed as lines of dots or hash signs.

Additionally, we attach an archive UDtrack_segmentations.zip, which contains the segmentations for each text file and the lemmas extracted from each text file, for visual inspection.

#Addendum by Aleksandrs Berdicevskis, 2019-10-31:
- if you want to skip calculating entropy of the segmented text (i.e. avoid the long process of morphological segmentation), run count_entropy_noder.py (in the same way as count_entropy.py)
