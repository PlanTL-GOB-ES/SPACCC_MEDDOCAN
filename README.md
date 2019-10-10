# SPACCC_MEDDOCAN: Spanish Clinical Case Corpus - Medical Document Anonymization

## Digital Object Identifier (DOI) and access to dataset files


## Introduction

This repository contains a synthetic corpus of clinical cases enriched with PHI expressions, named the MEDDOCAN corpus.

The final collection of 1,000 clinical cases that make up the corpus have around 33 thousand sentences, with an average 
of around 33 sentences per clinical case. The MEDDOCAN corpus contains around 495 thousand words, with an average of 494 
words per clinical case, slightly less than for the records of the i2b2 de-identification longitudinal corpus (617 tokens 
per record). The MEDDOCAN corpus is distributed in plain text in UTF8 encoding, where each clinical case is stored as a 
single text file, and PHI annotations are released in the popular BRAT format, which makes visualization of results 
straightforward.

## Repository structure

In this repository:

<pre>
script/
	CODALAB-Evaluation-Script/
		COBALAB version of the original evaluation script for the MEDDOCAN task.
	Format-Converter-Script/	
		Script to convert files between MEDDOCAN-Brat, MEDDOCAN-XML, and i2b2 formats.
</pre>


In Zenodo:

<pre>
corpus/
`Train`, `development`, and `test` data sets, both `BRAT` standoff format and `i2b2` format.

guidelines/
Annotation guidelines.

IAA/
Inter-annotator agreement report, along with the data and the scripts used to calculate it. 
</pre>


## Document selection

The SPACCC corpus was created after collecting 1,000 clinical cases from SciELO (Scientific Electronic Library Online), 
an electronic library that gathers electronic publications of complete full text articles from scientific journals of 
Latin America, South Africa and Spain (http://www.scielo.org).

A clinician classified those cases into those that were similar to real clinical texts in terms of structure and content
and those that were not suitable for this task. Figure legends were automatically removed and, in case multiple clinical 
cases were listed, these were split into single clinical cases.


## Annotation tool

The manual annotation of the entire corpus was carried out in a three-step approach. First, an initial annotation 
process was carried out on an adapted version of the `AnnotateIt tool`. The resulting annotations were then exported, 
trailing whitespaces were removed and double annotations of the same string were send as an alert to the human annotators
for revision/correction. Then, the annotations were uploaded into the `BRAT annotation tool`, which was slightly less 
efficient for mention labeling in terms of manual annotation speed. The human annotators performed afterwards a final 
revision of the annotations in `BRAT`, in order to correct mistakes and to add potentially missing annotation mentions. 
Finally the senior annotator did a last round of annotation revision of the entire corpus. 


## Annotation format

Annotations created for SPACCC_MEDDOCAN are provided in BRAT standoff format; i.e. the annotations are stored separately 
(in an `.ann` file) from the document text (a `.txt` file). 
These two files are associated by their base name; their file name without suffix is the same, for example, the file 
`es-S0004-06142005000200009-1.ann` contains the annotations for the file `es-S0004-06142005000200009-1.txt`. 
See http://brat.nlplab.org/standoff.html for further details on the brat standoff format. 



## Annotation types

The MEDDOCAN annotation scheme defines a total of 29 granular entity types grouped into more general parent classes. 

See guidelines in `guidelines/` folder for further details.


## Annotation guidelines

The annotation guidelines describe the criteria that have been followed to annotate the corpus, along with illustrative 
examples. 

The annotation process of the MEDDOCAN corpus was inspired initially by previous annotation schemes and corpora used for 
the i2b2 de-identification tracks, revising the guidelines used for these tracks, translating certain characteristics into 
Spanish and adapting them to the specificities and needs of our document collection and legislative framework. This adaptation 
was carried out in collaboration with practicing physicians, a team of annotators and the University Hospital 12 de Octubre. 

The adaptation, translation, and refinement of the guidelines was carried out on several random sample sets of the MEDDOCAN 
corpus and connected to an iterative process of annotation consistency analysis through inter-annotator agreement (IAA) 
calculation until a high annotation quality on terms of IAA was reached. 

Three cycles of refinement and IAA analysis were needed in order to reach the quality criteria required for this track, being 
in line with similar scores obtained for instance for i2b2. The final version of the used 28 pages annotation guidelines can 
be found in the `guidelines/` directory.

Guidelines have been written and developed in Spanish and are only available in Spanish.


## Corpus consistency

The final, inter-annotator agreement measure obtained for this corpus was calculated on a set of 50 records that were double 
annotated (blinded) by two different expert annotators, reaching a pairwise agreement of 98% on the exact entity mention 
comparison level together with the corresponding mention type labels.

See the inter-annotator agreement report (Informe_interagreement_CNIO_PlanTL_SEAD.pdf) included in folder `IAA`in Zenodo for 
further details.

## Contact

Montserrat Marimon (montserrat.marimon@bsc.es)


## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

You are free to:
Share — copy and redistribute the material in any medium or format
Adapt — remix, transform, and build upon the material for any purpose, even commercially.
Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more information, please see
<https://creativecommons.org/licenses/by/4.0/>

Copyright (c) 2019 Secretaría de Estado para el Avance Digital (SEAD)
