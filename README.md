# 🌳 CED: Catalog Extraction from Documents

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/ced-catalog-extraction-from-documents/catalog-extraction-on-chcatext)](https://paperswithcode.com/sota/catalog-extraction-on-chcatext?p=ced-catalog-extraction-from-documents)
[![arXiv](https://img.shields.io/badge/arXiv-2304.14662-b31b1b.svg)](https://arxiv.org/abs/2304.14662)

Rebuild document catalog tree structures from plain texts.

- 📃 This is the official implementation of the ICDAR'23 paper: [CED: Catalog Extraction from Documents](https://arxiv.org/abs/2304.14662)
- 📂 Data files are available at [releases/tag/data-v1](https://github.com/Spico197/CatalogExtraction/releases/tag/data-v1).
- 📦 Model weights and logs are available at [releases/tag/model-v1](https://github.com/Spico197/CatalogExtraction/releases/tag/model-v1).

## ✈️ Abilities

- Concatenate OCR text pieces
- Compose paragraphs from sequences
- Extract document catalogs from plain texts

## ⚙️ Installation

Make sure you have `torch>=1.9.1` installed.
- Python>=3.7
- torch>=1.9.1

```bash
# better to create new environment in case of any potential package version mismatch
$ conda create -n doctree python=3.7
$ conda activate doctree
# install pytorch
$ echo 'install pytorch from https://pytorch.org/'

# install basics
$ pip install -e .
# if you want to test and make development, use this command
$ pip install -e .[dev]
# if you want to deploy demo on your local machine, use this
$ pip install -e .[demo]
# if you want to do both development and demo deployment, use this
$ pip install -e .[all]
```

## 🚀 Quick Start

All task examples are listed in `examples/` .

### Concatenate text segments

- Train

```bash
# change setting file in `examples/text_concat/train/config.yaml`
$ bash examples/text_concat/train/run.sh
```

- Inference

```bash
# check `examples/text_concat/inference/run.sh` and change the task directory
$ bash examples/text_concat/inference/run.sh
```

### Concat & split paragraphs

We use the same task class to train paragraph split and text concatenation models

- Train

```bash
# change setting file in `examples/text_concat/train/config.yaml`
$ bash examples/text_concat/train/run.sh
```

- Inference

```bash
# check `examples/text_concat/inference/run.sh` and change the task directory
$ bash examples/text_concat/inference/run.sh
```

### Extract catalog structures

We use the hierarchical config mechanism in [REx](https://github.com/Spico197/REx).
Here, settings in `credit_eval.yaml` will override those in `base_config.yaml`.
You may want to add/change configurations in `credit_eval.yaml` to make it work.

- Train

```bash
# change setting file in `examples/doc_tree_construction/train/credit_eval.yaml`
$ bash examples/doc_tree_construction/train/run.sh
```

- Inference

```bash
# change `task_dir` in `examples/doc_tree_construction/inference/run_simple.py`
$ python examples/doc_tree_construction/inference/run_simple.py
```

## 📃 Documentations

Check `docs/` for more detailed explanations.

## 📜 Citation

If you find this paper or repo useful, please cite our paper:

```bibtex
@article{zhu2023ced,
  title={CED: Catalog Extraction from Documents},
  author={Zhu, Tong and Zhang, Guoliang and Li, Zechang and Yu, Zijian and Ren, Junfei and Wu, Mengsong and Wang, Zhefeng and Huai, Baoxing and Chao, Pingfu and Chen, Wenliang},
  journal={arXiv preprint arXiv:2304.14662},
  year={2023}
}
```
