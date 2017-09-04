```
   ______________  ______                __
  / ____/  _/ __ \/ ____/__  _  ______  / /___  ________  _____
 / /    / // /_/ / /   / _ \| |/_/ __ \/ / __ \/ ___/ _ \/ ___/
/ /____/ // _, _/ /___/  __/>  </ /_/ / / /_/ / /  /  __/ /
\____/___/_/ |_|\____/\___/_/|_/ .___/_/\____/_/   \___/_/
                              /_/
```

[![Build Status](https://travis-ci.org/YangLab/CIRCexplorer2.svg?branch=master)](https://travis-ci.org/YangLab/CIRCexplorer2)
[![Coverage Status](https://coveralls.io/repos/github/YangLab/CIRCexplorer2/badge.svg?branch=master)](https://coveralls.io/github/YangLab/CIRCexplorer2?branch=master)
[![Documentation Status](https://readthedocs.org/projects/circexplorer2/badge/?version=latest)](http://circexplorer2.readthedocs.org/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/circexplorer2.svg)](https://pypi.python.org/pypi/CIRCexplorer2)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](http://bioconda.github.io/recipes/circexplorer2/README.html)
[![Anaconda-Server Downloads](https://anaconda.org/bioconda/circexplorer2/badges/downloads.svg)](https://anaconda.org/bioconda/circexplorer2)
[![The MIT License](https://img.shields.io/badge/license-MIT-orange.svg)](https://github.com/YangLab/CIRCexplorer2/blob/master/LICENSE.txt)

CIRCexplorer2 is the successor of [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) with plenty of new features to facilitate circular RNA identification and characterization.

Authors: Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn), Li Yang (liyang@picb.ac.cn)

Maintainer: Xu-Kai Ma (maxukai@picb.ac.cn)

*NEWS*: 

From version 2.3.0, CIRCexplorer2 has very big changes in inputs and outputs.  For new structures, please see http://circexplorer2.readthedocs.org. If you want to check the information for old versions, please see http://circexplorer2.readthedocs.io/en/2.2.7 .

[CIRCpedia](http://www.picb.ac.cn/rnomics/circpedia) is an integrative database, aiming to annotating alternative back-splicing and alternative splicing in circRNAs across different cell lines. Welcome to use!

## Features

* Precisely annotate circular RNAs with [high accuracy, good sensitivity and low memory consumption](http://nar.oxfordjournals.org/content/44/6/e58.abstract)
* Support multiple circular RNA aligners (**TopHat2/TopHat-Fusion**, **STAR**, **MapSplice**, **BWA** and **segemehl**)
* *De novo* assemble novel circular RNA transcripts
* Characterize various of alternative (back-)splicing events of circular RNAs
* Fast identify circuar RNAs with **STAR** or **BWA**
* Support both single-read and paired-end sequencing.

CIRCexplorer2 documentation is available through https://readthedocs.org/ from [here](http://CIRCexplorer2.readthedocs.org), including installation instructions and tutorial.

## Citation

[Zhang XO\*, Dong R\*, Zhang Y\*, Zhang JL, Luo Z, Zhang J, Chen LL#, Yang L#. Diverse alternative back-splicing and alternative splicing landscape of circular RNAs. *Genome Res*, 2016, 26:1277-1287](http://genome.cshlp.org/content/26/9/1277.abstract)

## License

Copyright (C) 2016-2017 YangLab.  See the [LICENSE](https://github.com/YangLab/CIRCexplorer2/blob/master/LICENSE.txt)
file for license rights and limitations (MIT).
