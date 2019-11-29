## 2019, IWMLC
## Semenuks

### (1) prep for file processing
######
## getting the arguments from the command line
arguments = commandArgs(trailingOnly=TRUE)

## loading the necessary packages
library(udpipe)
library(plyr)

## arguments:
  ## turn on or off displaying what file on rn
  ## read all .connllu files or only some
  ## output file

display.progress = c(2,2) 
  ## displaying progress - see code readme
incl.excl = 'excl' 
what.files = c()
  ## including/excluding files
output.file = 'Semenuks_ID_calculations.csv'
  ## output file name
input.folder = ''
  ## folder with UD files
output.folder = ''
  ## folder where the output should be placed

## checking that everything is OK with the arguments that were passed down
if (length(arguments != 0)) {
  ## should it be printed what file is currently being processed?
  if (length(grep('--progress',arguments)) > 0) {
    display.progress = as.integer(unlist(strsplit(arguments[grep('--progress',arguments)+1][1],"")))
    if (F %in% (display.progress %in% 0:2)) {
      print('Error in setting display progress: not a possible value. Defaulting to "22".')
      display.progress = c(2,2)
    }
  }
  
  ## what files should be analyzed?
  if (length(grep('--files',arguments)) > 0) {
    if (arguments[grep('--files',arguments)+1][1] == 'incl') {
      incl.excl = 'incl'
      what.files = arguments[grepl('*\\.conllu',arguments)]
      if (length(what.files) == 0) {
        print('No files specified as included for analysis. Defaulting to including all *.conllu files in the directory.')
        incl.excl = 'excl'
        what.files = c()
      }
    } else if (arguments[grep('--files',arguments)+1][1] == 'excl') {
      incl.excl = 'excl'
      what.files = arguments[grepl('*\\.conllu',arguments)]
    } else {
      print('Error in selecting files for analysis: not a possible value. Defaulting to including all *.conllu files in the directory.')
    }
  }
  
  ## what should the name of the output file be?
  if (length(grep('--output$',arguments)) > 0) {
    output.file = arguments[grep('--output',arguments)+1][1]
  }
  
  ## where should the UD files be read from?
  if (length(grep('--inputf',arguments)) > 0) {
    input.folder = arguments[grep('--inputf',arguments)+1][1]
  }
  
  ## where should the output file be placed?
  if (length(grep('--outputf',arguments)) > 0) {
    output.folder = arguments[grep('--outputf',arguments)+1][1]
  }
  
}
######


### (2) reading the files
######
  ## moving to the folder where the UD files are located
if (nchar(input.folder)>0) {
  setwd(input.folder)
}

  ## reading the UD files
    ## inclusion/exclusion of files
if (incl.excl == 'incl') {
  files = what.files
} else {
  files = list.files(pattern = 'conllu')
  files = setdiff(files,what.files)
}

dataset = list()
  ## should it be printed that the files are being read?
if (display.progress[1]>0) {
  print('>> Reading files')
  print('===== ===== ===== =====')
}
  ## reading the files; should each individual file being read be displayed?
if (display.progress[1] == 2) {
  for (i in files) {
    print(i)
    dataset[[i]] = udpipe_read_conllu(i)
  }
} else {
  for (i in files) {
    dataset[[i]] = udpipe_read_conllu(i)
  }
}
  ## should it be printed that everything is read?
if (display.progress[1]>0) {
  print('>> All files are read')
  print('===== ===== ===== =====')
  print("                       ")
  print("                       ")
}

######


### (3) calculating the mean information density and the standard deviation
######
  ## creating a data frame where the output will be stored
uid.measures = data.frame(lang = names(dataset), S_id_mean = 0, S_id_sd = 0)

  ## should it be printed that the ID calculations are being performed
if (display.progress[2]>0) {
  print('>> Calculating information density mean and standard deviation')
  print('===== ===== ===== =====')
}

  ## calculating the mean and the standard deviation of information density on the syntactic level for each language
for (i in names(dataset)) {
  if (display.progress[2] == 2) {
    print(i)
  }
  
  temp = dataset[[i]]
  
    ## getting rid of all of the cases where a token is a (duplicated) combination of two other tokens (e.g. see tokens 2, 3 & 2-3 in sentence CF892-3 in Portuguese-Bosque data)
  temp$token_id = as.integer(temp$token_id)
  temp = subset(temp, !is.na(temp$token_id))
  
    ## removing sentences that contain tokens with X or SYM tags
      ## finding which sentence have them
  temp.sent.remove = ddply(temp, 'sentence_id', summarise, sym.x.in = ('X' %in% upos) | ('SYM' %in% upos))
  temp.sent.remove = subset(temp.sent.remove, sym.x.in)$sentence_id
      ## removing those sentences from the dataset
  temp = subset(temp, ! (sentence_id %in% temp.sent.remove))
  
    ## removing punctuation
  temp = subset(temp, upos != 'PUNCT')[,c('sentence_id','token_id','upos')]
    ## calcualting how many tokens are left
  temp.height = dim(temp)[1]
  
    ## creating a data frame to calculate trigram conditional probabilities of UPOS tokens
      ## sentence_id - what sentence the tokens belong to 
      ## token_id - number of the token in the sentence
      ## xi = word at position i ("current" word)
      ## xim1 = word at position i-1
      ## xim2 = word at position i-2
      ## xim3 = word at position i-3
  temp.df = data.frame(sentence_id = temp$sentence_id, token_id = temp$token_id, xi = temp$upos, xim1 = c("",temp[1:(temp.height-1),'upos']), xim2 = c("","",temp[1:(temp.height-2),'upos']), xim3 = c("","","",temp[1:(temp.height-3),'upos']), x=0)
      ## removing the first three words in all of the sentences (since we can't calculate trigram conditional probabilities for them within the same sentence); removing token_id afterwards as it won't be needed anymore
  temp.df = subset(temp.df, token_id > 3)
  temp.df$token_id = NULL
  
    ## calculating trigram conditional probabilities
      ## frequency of UPOS tag following a trigram
  temp.df = ddply(temp.df, c('xi','xim1','xim2','xim3'), summarise, freq = length(x))
      ## frequency of trigrams
  temp.df.dd = ddply(temp.df, c('xim1','xim2','xim3'), summarise, total.freq = sum(freq))
      ## joining the data frames
  temp.df = join(temp.df,temp.df.dd, by = c('xim1','xim2','xim3'))
      ## calculating the conditional probabilities: dividing the frequency of occurence of a UPOS tag following a trigram by the frequency of that trigram
  temp.df$prob = temp.df$freq/temp.df$total.freq
      ## calculating the suprisal based on conditional probability
  temp.df$inf = log(1/temp.df$prob)
  
  uid.measures[uid.measures$lang == i,'S_id_mean'] = mean(rep(temp.df$inf, temp.df$freq))
  uid.measures[uid.measures$lang == i,'S_id_sd'] = sd(rep(temp.df$inf, temp.df$freq))
}

  ## should it be printed that the ID calculations are finished?
if (display.progress[2]>0) {
  print('>> Information density calculations finished')
  print('===== ===== ===== =====')
  print("                       ")
  print("                       ")
}
######

### (4) saving the data
######
  ## moving to the folder where the output file should be written
if (nchar(output.folder)>0) {
  setwd(output.folder)
}

  ## writing the file
write.csv(x = uid.measures,file = output.file,row.names = F)
print(paste0('>> ',output.file,' is saved in ',output.folder,collapse=""))
######