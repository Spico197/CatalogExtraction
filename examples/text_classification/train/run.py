from omegaconf import OmegaConf
from rex.utils.config import ConfigParser
from rex.utils.logging import logger
from rex.utils.initialization import init_all

from doctree.tasks.text_classification import TextClassificationTask


def main():
    config = ConfigParser.parse_cmd()
    init_all(config.task_dir, config.random_seed, True, config)
    logger.info(OmegaConf.to_object(config))
    task = TextClassificationTask(config)
    logger.info(f"task: {type(task)}")

    logger.info("Start Training")
    task.train()
    task.print_final_record()

    logger.info("Start Test")
    task.load(config.final_eval_model_filepath)
    task.eval("test", verbose=True)


if __name__ == "__main__":
    main()
