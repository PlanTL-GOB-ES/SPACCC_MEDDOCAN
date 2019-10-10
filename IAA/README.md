# Inter-annotator agreement

The inter-annotator agreement report, along with the data and the scripts that have been used to calculate it. 


## Directory structure

* `des_an1_an2.csv`: table of results of interagreement between Annotator 1 and Annotator 2 on the development corpus.
* `des_an1_fre.csv`: table of results of interagreement between Anotador 1 and SPACCC_POS-TAGGER on the development corpus.
* `des_an2_fre.csv`: table of results of interagreement between Anotador 2 and SPACCC_POS-TAGGER on the development corpus.
* `des_arm_fre.csv`: table of results of interagreement between the gold standard corpus and SPACCC_POS-TAGGER on the development corpus.
* `indice_informe_interagreement.txt`: validated index for the inter-anotator agreement report.
* `Informe_interagreement_CNIO_PlanTL_SEAD.pdf`: report that shows the agreement and discrepancies between the two annotators and between them and SPACCC_POS-TAGGER.
* `main.py`: script to calculate the inter-annotator agreement.
* `README.md`: this file.
* `script.py`: auxiliary script to calculate the inter-annotator agreement.
* `val_an1_fre.csv`: table of results of interagreement between Anotador 1 and SPACCC_POS-TAGGER on the validation corpus.


## Usage

### Prerequisites

The script to calculate the inter-annotator agreement requires Python 3 installed on your system. 

### Calculation of the table of results of interagreement between 2 corpora

To obtain the results table by comparing 2 different annotations, you must execute the script with the name of the output file and the 2 data folders as parameters.

### Example

Assuming that: 
- the results table will be named "des_an1_an2.csv"
- the corpus of Annotator 1 is in folder "anotador1/"
- the corpus of Annotator 2 is in folder "anotador2/"

Use the following command:
<pre>
python3 main.py des_an1_an2.csv anotador1/ anotador2/
</pre>

