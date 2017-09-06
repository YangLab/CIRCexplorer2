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
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](http://bioconda.github.io/recipes/circexplorer2/README.html)
[![Anaconda-Server Downloads](https://anaconda.org/bioconda/circexplorer2/badges/downloads.svg)](https://anaconda.org/bioconda/circexplorer2)
[![The MIT License](https://img.shields.io/badge/license-MIT-orange.svg)](https://github.com/YangLab/CIRCexplorer2/blob/master/LICENSE.txt)

CIRCexplorer2 is a comprehensive and integrative circular RNA analysis toolset. It is the successor of [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) with plenty of new features to facilitate circular RNA identification and characterization.

Authors: Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn), Li Yang (liyang@picb.ac.cn)

Maintainer: Xu-Kai Ma (maxukai@picb.ac.cn)

*NEWS*: 

From version 2.3.0, CIRCexplorer2 has very big changes in inputs and outputs.  For new structures, please see http://circexplorer2.readthedocs.org. If you want to check the information for old versions, please see http://circexplorer2.readthedocs.io/en/2.2.7 .

[CIRCpedia](http://www.picb.ac.cn/rnomics/circpedia) is an integrative database, aiming to annotating alternative back-splicing and alternative splicing in circRNAs across different cell lines. Welcome to use!

## Features

* Precisely annotate circular RNAs ([Annotate](modules/annotate.md))
* Support multiple circular RNA aligners (**TopHat2/TopHat-Fusion**, **STAR**, **MapSplice**, **BWA** and **segemehl**) ([Align](modules/align.md) and [Parse](modules/parse.md))
* *De novo* assemble novel circular RNA transcripts ([Assemble](modules/assemble.md))
* Characterize various of alternative (back-)splicing events of circular RNAs ([Denovo](modules/denovo.md))
* Fast identify circuar RNAs with [STAR](https://github.com/alexdobin/STAR) or [BWA](https://github.com/lh3/bwa) ([Parse](modules/parse.md))
* Support both single-read and paired-end sequencing.

*For some frequently asked questions about CIRCexplorer2, please [FAQ](about/faq.md) for more details.*

## Tutorial

We have developed a fairly comprehensive tutorial that demonstrates how CIRCexplorer2 helps you to promote your research in circular RNA identification and characterization. Please check it below!

* [Installation and Setup](tutorial/setup.md)
* [Pipeline](tutorial/pipeline.md)
* [Alignment](tutorial/alignment.md)
* [Parsing](tutorial/parsing.md)
* [Annotating](tutorial/annotating.md)
* [Assembly](tutorial/assembly.md)
* [Alternative Splicing](tutorial/as.md)

We also offered `fast_circ.py` script to help you to automatically run our pipelines in one step without any additional operations. Please check this [one-step script](tutorial/one_step.md) for more details.

## Modules

CIRCexplorer2 contains 5 modules. Each module functions as an independent component owning its distinctive duty. Meanwhile, they inteact with each other, and different circular RNA analysis pipelines are derived from different combinations of several modules. Understanding the detailed mechanism of each module could facilitate your circular RNA research.

List of Modules:

* [Align](modules/align.md)
* [Parse](modules/parse.md)
* [Annotate](modules/annotate.md)
* [Assemble](modules/assemble.md)
* [Denovo](modules/denovo.md)

## Related tools

We developed a series of circular RNA analysis tools, and welcome to use and cite our work. See [Related Tools](about/tools.md) for more information.

## Citation

[Zhang XO\*, Dong R\*, Zhang Y\*, Zhang JL, Luo Z, Zhang J, Chen LL#, Yang L#. Diverse alternative back-splicing and alternative splicing landscape of circular RNAs. *Genome Res*, 2016, 26:1277-1287](http://genome.cshlp.org/content/26/9/1277.abstract)

## License

Copyright (C) 2016-2017 YangLab. See [LICENSE](about/license.md) for license rights and limitations (MIT).
