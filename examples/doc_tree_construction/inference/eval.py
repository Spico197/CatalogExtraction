from collections import defaultdict

import numpy as np

from doctree.tasks.transducer_task import TransducerDocTreeConstructionTask


def main():
    # src -> tgt -> seed
    overall_f1s = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1)))
    seeds = [17, 127, 1227, 12227, 122227]
    datanames = ["BidAnn", "FinAnn", "CreRat"]

    for src in datanames:
        for seed in seeds:
            task = TransducerDocTreeConstructionTask.from_taskdir(f"paper_outputs/transducer_5_{src}_{seed}")
            task.config.skip_train = True
            task.load_best_ckpt()
            for tgt in datanames:
                print(f"src: {src}, tgt: {tgt}, seed: {seed}")
                task.config.test_filepath = f"data/doc_tree_construct/Paper/{tgt}/test.jsonl"
                measures = task.hierarchical_eval("test")
                overall_f1s[src][tgt][seed] = measures["overall"]["f1"]

    print(f"{overall_f1s}")

    for tgt in datanames:
        for src in datanames:
            _group = []
            for seed in seeds:
                val = overall_f1s[src][tgt][seed]
                _group.append(val)
                print(val)
            print(np.mean(_group))
            print(np.std(_group))
            print("")


if __name__ == "__main__":
    main()
