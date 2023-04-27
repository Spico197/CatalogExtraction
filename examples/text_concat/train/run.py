from rex.utils.config import ConfigParser

from doctree.tasks.text_concat_task import TextConcatTask


def main():
    config = ConfigParser.parse_cmd()

    train_tool = TextConcatTask.from_config(config)

    # mode: "train" or "test"
    if train_tool.config.mode == "train":
        train_tool.train()

    train_tool.load_best_ckpt()
    ACC, eval_loss, all_answer = train_tool.eval("test")
    print(f"Trial Finished, {ACC}")


if __name__ == "__main__":
    main()
