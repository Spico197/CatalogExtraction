from pathlib import Path

from rex.utils.config import ConfigParser
from rex.utils.logging import logger
from doctree.tasks.transducer_task import TransducerDocTreeConstructionTask


def main():
    config = ConfigParser.parse_cmd(
        # cmd_args="-b examples/doc_tree_construction/train/base_config.yaml -c examples/doc_tree_construction/train/domain.yaml".split()
    )
    task = TransducerDocTreeConstructionTask.from_config(config)
    logger.info(f"task: {type(task)}")

    # if (
    #     "load_pretrained_model" in config
    #     and config.load_pretrained_model
    #     and "pretrained_model_path" in config
    #     and Path(config.pretrained_model_path).exists()
    # ):
    #     # load model
    #     task.load_pretrained_model(config.pretrained_model_path)

    if not task.config.skip_train:
        logger.info("Start Training")
        task.train()

    task.load_best_ckpt()

    if not task.config.skip_further_train:
        task.history = {"train": [], "dev": [], "test": []}
        task.no_climbing_cnt = 0
        task.best_metric = -100.0
        task.best_epoch = -1

        logger.info("Start Further Training")
        task.train()

    measures = task.eval("test")
    logger.info(task.transform.action2label.label2id)
    logger.info(f"test_measures: {measures}")

    task.hierarchical_eval("test")


if __name__ == "__main__":
    main()
