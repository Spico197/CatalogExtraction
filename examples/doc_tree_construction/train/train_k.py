"""train_k: 只用k篇src文档训练，在tgt上预测"""

import os
from collections import defaultdict

import numpy as np
from rex.utils.config import ConfigParser

from doctree.tasks.transducer_task import TransducerDocTreeConstructionTask


def main(k=-1, use_wikibert=False):
    print(f"train_k: {k}, wikibert: {use_wikibert} train on all src")
    overall_f1s = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
    seeds = [17, 127, 1227, 12227, 122227]
    datanames = ["BidAnn", "FinAnn", "CreRat"]

    for src in datanames:
        for seed in seeds:
            print(f"Training on {src}, seed: {seed}")
            config = ConfigParser.parse_cmd(
                cmd_args=[
                    "-b", "examples/doc_tree_construction/train/base_config.yaml",
                    "-c", "examples/doc_tree_construction/train/custom.yaml"
                ]
            )
            if use_wikibert:
                config.plm_dir = "data/wiki_plm_4w"
                config.name = f"transducer_wikibert_trainOn{k}_{src}_{seed}"
            else:
                config.plm_dir = "/data4/tzhu/bert_pretrained_models/hfl_rbt3"
                config.name = f"transducer_trainOn{k}_{src}_{seed}"
            config.task_dir = f"paper_outputs/{config.name}"
            config.train_docs = k
            config.data_type = src
            config.data_dir = f"data/doc_tree_construct/Paper/{src}"
            config.debug_mode = False
            config.device = "cuda:0"
            config.random_seed = seed
            task = TransducerDocTreeConstructionTask.from_config(config)
            task.train()
            task.load_best_ckpt()
            measures = task.hierarchical_eval("test")
            overall_f1s[src][src][seed] = measures["overall"]["f1"]
            print(f"src: {src}, tgt: {src}, seed: {seed}, f1: {overall_f1s[src][src][seed]}")
            for tgt in datanames:
                if src != tgt:
                    task.config.test_filepath = f"data/doc_tree_construct/Paper/{tgt}/test.jsonl"
                    measures = task.hierarchical_eval("test")
                    overall_f1s[src][tgt][seed] = measures["overall"]["f1"]
                    print(f"src: {src}, tgt: {tgt}, seed: {seed}, f1: {overall_f1s[src][tgt][seed]}")

    print(overall_f1s)
    for tgt in datanames:
        for src in datanames:
            print(f"tgt: {tgt}, src: {src}")
            _group = []
            for seed in seeds:
                val = overall_f1s[src][tgt][seed]
                _group.append(val)
                print(val)
            print(np.mean(_group))
            print(np.std(_group))
            print("")

    print(f"Finished! train_k: {k}, wikibert: {use_wikibert} train on all src")


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "2"
    # main(k=3, use_wikibert=False)
    # main(k=10, use_wikibert=False)
    # main(k=3, use_wikibert=True)
    # main(k=10, use_wikibert=True)
