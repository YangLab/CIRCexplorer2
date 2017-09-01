## 2.3.0 (2017-09-01)

Improvements:

* reorganize inputs and outputs.
* add alternative back-splicing analysis
* support Python 3

Bugfixes:

* bug in align step

## 2.2.7 (2017-07-20)

Bugfixes:

* fix a display error in assemble step
* fix a bug with "--low-confidence" option in annotate step

## 2.2.6 (2016-09-25)

Bugfixes:

* bug in building bowtie1/2 index using multiple threads
* bug in parsing Drosophila circRNAs

## 2.2.5 (2016-09-17)

Improvements:

* let fetch_ucsc.py support mm9

## 2.2.4 (2016-09-02)

Bugfixes:

* fix a bug in align module

## 2.2.3 (2016-08-19)

Bugfixes:

* fix a bug in align module

## 2.2.2 (2016-08-16)

Improvements:

* update logic of annotate step
* update build index module

## 2.2.1 (2016-08-08)

Improvements:

* chang option '-p' to '--pe' in parse module
* add 'fast_circ.py'

Bugfixes:

* bug in align module because of parse module

## 2.2.0 (2016-08-04)

Improvements:

* add paired-end data parsing function

## 2.1.2 (2016-07-22)

Improvements:

* add '--low-confidence' option

## 2.1.1 (2016-07-20)

Bugfixes:

* bug that ignores case-sensitivity in fusion fix step

Improvements:

* improve fusion junction identification efficiency for BWA

## 2.1.0 (2016-07-04)

Improvements:

* support for BWA

Bugfixes:

* change module name from 'circ' to 'circ2' in case of conflict with CIRCexplorer (issue #1).

## 2.0.1 (2016-06-21)

Improvements:

* test on PyPI and Bioconda
* lots of code improvements

## 2.0.0 (2016-04-05)

Features:

* pre-release for CIRCexplorer2
