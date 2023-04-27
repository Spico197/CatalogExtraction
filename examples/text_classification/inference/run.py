import time

from rex.utils.config import ConfigParser
from rex.utils.initialization import init_all
from omegaconf import OmegaConf
from rex.utils.logging import logger
from rex.utils.io import load_json
from tqdm import tqdm

from doctree.tasks.text_classification import TextClassificationTask


def main():
    # 加载模型
    config = ConfigParser.parse_cmd()
    init_all(config.task_dir, config.random_seed, True, config)
    logger.info(OmegaConf.to_object(config))
    task = TextClassificationTask(config)
    logger.info(f"task: {type(task)}")
    task.load(config.final_eval_model_filepath)

    # 还原一篇文档，得到树的ROOT Node
    # 要求输入为List[text]
    texts = """石家庄污水处理有限公司桥西污水处理厂2021-2022年度一、二期水源热泵运营管理服务项目比选公告
1. 招标条件
本招标项目河北建设投资集团有限责任公司在老挝投资建设60MW怀拉涅河水力发电项目已由河北省发展和改革委员会以冀发改外资备【2017】32号批准建设，项目业主为Houay LaNge Power Co,Ltd，建设资金来自企业自筹，项目出资比例为100%，招标人为建投国际投资有限公司。项目已具备招标条件，现对该项目的设计施工总承包进行公开招标。

2. 项目概况与招标范围
2.1项目概况：老挝怀拉涅河水电项目位于老挝东南部色贡省格林县境内怀拉涅河上，距下游薄冰村两公里，距格林县公路里程70公里，距色贡省会班蓬180公里，距沙拉湾公路里程210公里，距巴色市公路里程290公里。本水电站是一级开发方案中的唯一电站，装机容量60MW，装机年利用小时数4896小时，多年平均发电量2.9375亿kW·h，输电线路长度约41Km。

2.2招标范围：承包商依据招标文件的要求完成老挝新建 H.La-Nge 水电站至 Nam E-Moun 变电站 220kV 单回路输电线路勘察、施工图设计、建安施工、设备和材料采购、项目管理、排雷、调试以及竣工移交、缺陷修复、技术服务、人员培训、电网验收、试运行等全过程工作，以及为线路投入并网运行与越南电网的联系沟通及各种手续和批准性文件的获取工作；此项目为交钥匙工程。。

3. 投标人资格要求
3.1 本次招标对投标人的资格要求如下:

3.1.1资质要求:（1）投标人必须具有中华人民共和国企业法人资格，须具有商务部对外工程承包资格备案。 （2）投标人须具有建设行政主管部门核发的电力工程施工总承包二级及以上资质或输变电工程专业承包一级及以上资质； （3）必须具有建设行政主管部门核发的安全生产许可证（有效期内）。 （4）必须具有质量管理体系认证证书、职业健康安全管理体系认证证书、环境管理体系认证证书（有效期内）。

3.1.2业绩要求:具有同类工程项目业绩：具有同类工程项目业绩：2016年1月1日至2021年1月1日，在老挝至少具有1个已完成的110Kv及以上电力线路工程施工业绩，并在人员、设备、资金等方面具有相应的施工能力(投标人应在投标文件中提供类似业绩和工程接收证书（工程竣工验收证书）的合同的复印件)。

3.1.3项目负责人资格要求:投标人拟派项目经理具备机电工程注册建造师一级及以上执业资格和有效的安全生产考核合格证书（B本）。。

3.2 本次招标不接受联合体投标。

4. 招标文件的获取
4.1 凡有意参加投标者，请于2021-10-25 00:00至2021-10-30 00:00（北京时间，下同），登录惠招标下载电子招标文件。

4.2 招标文件每套售价0元，售后不退。技术资料押金0元，在退还技术资料时退还（不计利息）。

5. 投标文件的递交
5.1 投标文件递交的截止时间为2021-11-15 09:00:00，投标人应在截止时间前通过惠招标平台递交电子投标文件。

5.2 逾期送达的投标文件，电子招标投标交易平台将予以拒收。

6. 发布公告的媒介
本次招标公告同时在“河北省招标投标公共服务平台”、“石家庄市公共资源交易平 台”、“惠招标电子招标投标平台”上发布。

7.联系方式
招标人： 建投国际投资有限公司

招标代理机构： 北京兴电国际工程管理有限公司

地址： 石家庄市裕华西路9号裕园广场A座

地址： 北京市海淀区首体南路9号中国电工大厦7层01""".split(
        "\n"
    )
    texts = list(filter(lambda x: len(x) > 0, texts))
    num_predict_times = 100
    tot_time = 0.0
    for i in range(num_predict_times):
        stime = time.time()
        _ = task.predict(texts)
        utime = time.time() - stime
        tot_time += utime
    logger.info(
        f"Sync: #Prediction: {num_predict_times}, Total Time: {tot_time:.3f} s, MEAN: {tot_time/num_predict_times:.3f} s/doc"
    )
    root_node, _ = task.predict(texts)
    print(root_node.traverse())

    # 测试特定数据集下恢复一篇文档平均时间，并测试该数据集中多少文档能完全还原
    filepath = "/data2/jfren/work/DocTree/data/text_classification/mix_all/test.json"
    data_gold = load_json(filepath)
    doc_num = len(data_gold)
    count = 0
    total_time = 0
    for doc in tqdm(data_gold):
        texts = []
        for sent in doc["sents"]:
            texts.append(sent["text"])
        start_time = time.time()
        root_node, pre_data = task.predict(texts)
        end_time = time.time()
        utime = end_time - start_time
        total_time += utime
        if pre_data == doc["sents"]:
            count += 1
    avg_time = total_time / doc_num
    acc = count / doc_num
    print(
        f"doc_num : {doc_num} , right_count : {count} , acc : {acc} , total_time : {total_time:.3f} s , avg_time : {avg_time:.3f} s/doc"
    )


if __name__ == "__main__":
    main()
