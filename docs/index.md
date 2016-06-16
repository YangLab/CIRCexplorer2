
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

CIRCexplorer2 is a comprehensive and integrative circular RNA analysis toolset. It is the successor of [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) with plenty of new features to facilitate circular RNA identification and characterization.

## Features

* Support multiple circular RNA aligners (TopHat/TopHat-Fusion, STAR, MapSplice and segemehl)
* *De novo* assemble novel circular RNA transcripts
* Characterize various of alternative splicing events of circular RNAs

## Tutorial

We have developed a fairly comprehensive tutorial that demonstrates how CIRCexplorer2 helps you to promote your research in circular RNA identification and characterization. Please check it below!

* [Installation and Setup](tutorial/setup.md)
* [Pipeline](tutorial/pipeline.md)
* [Alignment](tutorial/alignment.md)
* [Annotating](tutorial/annotating.md)
* [Assembly](tutorial/assembly.md)
* [Alternative Splicing](tutorial/as.md)

You could check [FAQ](about/faq.md) for more details.

## Modules

CIRCexplorer2 contains 5 modules. Each module functions as an independent component owning its distinctive duty. Meanwhile, they inteact with each other, and different circular RNA analysis pipelines are derived from different combinations of several modules. Understanding the detailed mechanism of each module could facilitate your circular RNA research.

List of Modules:

* [Align](modules/align.md)
* [Parse](modules/parse.md)
* [Annotate](modules/annotate.md)
* [Assemble](modules/assemble.md)
* [Denovo](modules/denovo.md)

## Citation

Zhang XO\*, Dong R\*, Zhang Y\*, Zhang JL, Luo Z, Zhang J, Chen LL#, Yang L#. Diverse alternative back-splicing and alternative splcing landscape of circular RNAs. *under review*

We developed a series of circular RNA analysis tools, and welcome to use and cite our work. See [Citation](about/citation.md) for more information.

## License

Copyright (C) 2016 YangLab. See [LICENSE](about/license.md) for license rights and limitations (MIT).
