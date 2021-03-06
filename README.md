# DrugEx+R
[![License](https://img.shields.io/github/license/naisuu/drugex-plus-r)](https://github.com/naisuu/drugex-plus-r/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) 
[![version](https://img.shields.io/github/v/release/naisuu/drugex-plus-r)](https://github.com/naisuu/drugex-plus-r/releases)

DrugEx+R was created for the purpose of experimenting with the development and implementation of retrosynthesis engines within molecular generators for the goal of de novo drug design; the focus of [my Master's thesis](TODO).
The code in this repository is based on [DrugEx v2](https://github.com/XuhanLiu/DrugEx), released by Xuhan Liu (First Author) and Gerard J.P. van Westen (Correspondent Author) on March 8th, 2021. The same license terms apply for this repository, and can be found in the LICENSE file.

## Getting started
After cloning this repository, make sure you have a conda distribution installed. We recommend [miniforge](https://github.com/conda-forge/miniforge) for licensing reasons, but anaconda/miniconda will work as well.

### Installing the environment
- `conda env create -f environment.yml`
- `conda activate drugexr`
- `pip install -e .`

#### Mamba
Mamba is a drop-in replacement for conda, it's much faster at resolving environments and is recommended.
You can install it by running `conda install -c conda-forge mamba`.
In case you want to use this from the start, replace `conda` with `mamba` in the instructions above.

# Data Version Control (DVC)
This project uses DVC to version control large data files and trained models on [DagsHub](https://dagshub.com/naisuu/drugex-plus-r).
To use DVC, run the following commands:
- `conda install -c conda-forge mamba`
- `mamba install -c conda-forge dvc`


# Known development issues
- black requires specific versions of typing-extensions, so you may need to run ```pip install typing-extensions --upgrade``` first.
- If you are developing on a mac, you may run into issues with xgboost. To fix this, you need to have cmake installed, which can be done by running the following commands (assuming you have brew installed): `brew install gcc@11`, followed by `brew install cmake`. Note that because RA Score has a hard dependency on tensorflow-gpu to run their pretrained models, development on a mac is currently limited to just the base functionality of DrugEx+R (unless you have a CUDA-compatible GPU).

# Additional information
The paper that accompanies the original DrugEx v2 code can be found [here](https://chemrxiv.org/engage/chemrxiv/article-details/60c75834469df47f67f455b9).
