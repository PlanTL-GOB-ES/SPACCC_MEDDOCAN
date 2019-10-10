# MEDDOCAN: Evaluation Script (CODALAB version)

## Digital Object Identifier (DOI)


## Introduction
This script is the COBALAB version of the original evaluation script. It
has been adapted to fit the requirements of the platform, but otherwise, 
it works exactly like the original script.

It is distributed as apart of the Medical Document Anonymization
(MEDDOCAN) task. It is based on the evaluation script from the i2b2 2014
Cardiac Risk and Personal Health-care Information (PHI) tasks. It is
intended to be used via command line:

<pre>
$> python evaluate.py input_folder/ output_folder/
</pre>

It produces Precision, Recall and F1 (P/R/F1) and leak score measures for
the NER subtrack and P/R/F1 for the SPAN subtrack. The latter includes an
additional metric where the spans are merged if only non-alphanumerical
characters are found between them.

## Prerequisites

This software requires to have Python 3 installed on your system.


## Directory structure

<pre>
annotated_corpora/
This directory contains files with annotations Brat annotation format. It may contain
different sub-directories for different annotation levels: tokens, sentence splitting,
part-of-speech taggin, etc. The sub-directory `sentence_splitting` is mandatory to 
compute the `leak score` evaluation metric. These files must be stored with `.ann` 
suffix.

input/
This directory contains the gold standard files and the systems submission files (in this
distribution we include five document from the development set). 
Gold standard files must be placed under the `ref` directory and 
system files (User submission) under the `res` directory. 
The `ref` directory contains two subdirectories with the files in `brat` and `xml` formats. 
The `res` directory can contain two subdirectories with the files in `brat` and `xml` formats, 
and at least one of them is required.
In this evaluation, we have two tasks (`subtask1` and `subtask2`), 
therefore the res directory should follow the below structure 
(In this example we show `brat` format, you can submit `xml` format):
|- res
     |- brat
           |- subtask1
                  | - S0004-06142005000500011-1.ann
                  | - S0004-06142005000500011-1.txt
                  |- ...
           |- subtask2
                  |- S0004-06142005000500011-1.ann
                  |- S0004-06142005000500011-1.txt
                  |- ...

Files in the previous directories must be in the appropriate format: `.ann` 
and `.txt` for `brat`, and `.xml` for `xml`. 

Note1: the `brat` format is used by the script. 
Note2: Users must put all annotated files that exist in `ref` directory under `res` directory,
 otherwise they could not see their results.

output/
This directory where the script outputs the results for the run.


## Usage

The user can select different folders using the command line:

<pre>
usage: evaluate.py input_folder/ output_folder/
</pre>


## Contact
Siamak Barzegar (siamak.barzegar@bsc.es)


## License

Copyright (c) 2019 Secretaría de Estado para el Avance Digital (SEAD)

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

