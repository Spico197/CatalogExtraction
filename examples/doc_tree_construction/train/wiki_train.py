import os
from collections import defaultdict

import numpy as np
from rex.utils.config import ConfigParser

from doctree.tasks.transducer_task import TransducerDocTreeConstructionTask


def main():
    print("wikibert train on all src")
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
            config.name = f"transducer_wikibert_trainOnAll_{src}_{seed}"
            config.task_dir = f"paper_outputs/{config.name}"
            config.train_docs = -1
            config.data_type = src
            config.data_dir = f"data/doc_tree_construct/Paper/{src}"
            config.debug_mode = False
            config.device = "cuda:0"
            config.random_seed = seed
            config.plm_dir = "data/wiki_plm_4w"
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

    print("Finished: wikibert train on all src")


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "2"
    main()
