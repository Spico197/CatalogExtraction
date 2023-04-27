"""then_train_k: src训练，k篇tgt上再训练，tgt上推理"""

import os
from collections import defaultdict

import numpy as np
from omegaconf import OmegaConf
from doctree.tasks.transducer_task import TransducerDocTreeConstructionTask


def main(k, use_wikibert=False):
    print(f"then_train_k: {k}, wikibert: {use_wikibert} train on all src")
    overall_f1s = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
    seeds = [17, 127, 1227, 12227, 122227]
    datanames = ["BidAnn", "FinAnn", "CreRat"]

    for src in datanames:
        for tgt in datanames:
            if src != tgt:
                for seed in seeds:
                    if use_wikibert:
                        task_name = f"transducer_wikibert_trainOnAll_{src}_thenTrainOn{k}_{tgt}_{seed}"
                    else:
                        task_name = f"transducer_trainOnAll_{src}_thenTrainOn{k}_{tgt}_{seed}"
                    config_filepath = f"paper_outputs/{task_name}/task_params.yaml"
                    config = OmegaConf.load(config_filepath)
                    config.name = task_name
                    config.task_dir = f"paper_outputs/{task_name}"
                    config.train_docs = k
                    config.data_type = tgt
                    config.data_dir = f"data/doc_tree_construct/Paper/{tgt}"
                    config.debug_mode = False
                    config.device = "cuda:0"
                    config.random_seed = seed
                    for part in ["train", "dev", "test"]:
                        config[f"{part}_filepath"] = f"data/doc_tree_construct/Paper/{tgt}/{part}.jsonl"

                    task = TransducerDocTreeConstructionTask.from_config(config)
                    task.load_best_ckpt()
                    task.train()
                    measures = task.hierarchical_eval("test")
                    overall_f1s[src][tgt][seed] = measures["overall"]["f1"]

    print(overall_f1s)
    for tgt in datanames:
        for src in datanames:
            if src != tgt:
                print(f"tgt: {tgt}, src: {src}")
                _group = []
                for seed in seeds:
                    val = overall_f1s[src][tgt][seed]
                    _group.append(val)
                    print(val)
                print(np.mean(_group))
                print(np.std(_group))
                print("")

    print(f"Finished! then_train_k: {k}, wikibert: {use_wikibert} train on all src")


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    # main(k=3, use_wikibert=False)
    main(k=10, use_wikibert=False)
    main(k=3, use_wikibert=True)
    main(k=10, use_wikibert=True)
