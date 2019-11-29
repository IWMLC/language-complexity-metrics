1. Code requirements:
  1.1. Programming language: R (version 3.5.3 (2019-03-11) used)
  1.2. Additional packages: udpipe (version 0.8.2 used); plyr (version 1.8.4 used)
  1.3. The code was tested in macOS Mojave, version 10.14.4

2. Execution of the code from the command line
  2.1. Running the code can be accomplished by typing Rscript 2019_IWMLC_Semenuks_script.R [arguments] in the command line. The arguments are explained below
  2.2. Arguments and their defaults
    Note: all of the arguments below have defaults, so they don't necessarily need to be specified. Additionally, the arguments can be written in any order (as long as the values for arguments are written immediately after their tags, e.g. [--files excl A.conllu --output test.csv] will work, but [--files --output excl A.conllu test.csv] will not).

    2.2.1. Input folder
           All of the files for which the information density mean and standard deviation are calculated should be located in the folder specified after the [--inputf] tag.

           For example,
           Rscript 2019_IWMLC_Semenuks_script.R --inputf ~/Documents/ID-Complexity/Data
           will read the files from the folder ~/Documents/ID-Complexity/Data

           Default value: the working directory in the command line

    2.2.2. Include/exclude files from being read
           Only certain files in the folder can be specified to be read and analyzed by including the [--files] tag.

           To include only certain files from the input folder:
           Rscript 2019_IWMLC_Semenuks_script.R --files incl <file names separated by space>

           To exclude files from the folder:
           Rscript 2019_IWMLC_Semenuks_script.R --files excl <file names separated by space>

           Default value: read/analyze all of the files in the input folder

    2.2.3. Output folder
           [--outputf] specifies the output folder where the calculated values will be recorded.

           Default value: the working directory in the command line

    2.2.4. Output file name
           [--output] specified the name of the output file.

           Default value: Semenuks_ID_calculations.csv
