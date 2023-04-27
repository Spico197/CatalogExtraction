from rex.utils.config import ConfigParser
from rex.utils.logging import logger
from doctree.tasks.transducer_task import TransducerDocTreeConstructionTask


def main():
    config = ConfigParser.parse_cmd(
        cmd_args=(
            " -b examples/doc_tree_construction/train/base_config.yaml"
            " -c paper_outputs/transducer_wiki_pretrain_again/task_params.yaml"
        ).split()
    )
    task = TransducerDocTreeConstructionTask.from_config(config)
    logger.info(f"task: {type(task)}")

    input_filepath = "paper_outputs/transducer_wiki_pretrain_again/ckpt/TransducerWithBert.step.9999.pth"
    output_dir = "data/wiki_plm_1w"

    task.load(input_filepath)
    task.model.encoder.save_pretrained(output_dir)
    task.model.encoder.config.save_pretrained(output_dir)
    task.transform.tokenizer.save_pretrained(output_dir)


if __name__ == "__main__":
    main()
