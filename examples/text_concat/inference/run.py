from rex.utils.logging import logger

from doctree.tasks.text_concat_task import TextConcatTask
from doctree.utils import content_tool as C


def main():
    task_dir = "outputs/text_concat"
    text_task = TextConcatTask.from_taskdir(
        task_dir,
        load_best_model=True,
        load_best_optimizer=False,
        load_train_data=False,
        load_dev_data=False,
        load_test_data=False,
        initialize=False,
        makedirs=False,
        dump_configfile=False,
    )

    task_dir = "outputs/paragraph_split"
    paragraph_task = TextConcatTask.from_taskdir(
        task_dir,
        load_best_model=True,
        load_best_optimizer=False,
        load_train_data=False,
        load_dev_data=False,
        load_test_data=False,
        initialize=False,
        makedirs=False,
        dump_configfile=False,
    )

    """
    输入形式：json文件地址
    """

    file_path = "data/ocr_recognised_results/A_result/2020-08-19-2005835.json"
    json_data = C.extract_content_from_file(file_path)
    logger.info(f"Raw Data: {json_data}")

    # 从原始json文件中提取内容并生成句子对数据
    pair_data_for_concat = C.get_pair_for_concat(json_data)
    # 判断文本合并
    pred_concat_result = text_task.predict_batch(pair_data_for_concat)
    # 根据结果对文本进行合并
    concat_result = C.merge_pair_text(pred_concat_result)
    logger.info(f"OCR Merged Data: {concat_result}")

    # 从文本合并结果得到段落分割句子对数据
    pair_data4split = C.get_pair_for_split(concat_result)
    # 判断段落分割
    pred_split_result = paragraph_task.predict_batch(pair_data4split)
    # 根据结果生成段落
    paragraph_list = C.merge_pair_text(pred_split_result)
    logger.info(f"Paragraph Data: {paragraph_list}")


if __name__ == "__main__":
    main()
