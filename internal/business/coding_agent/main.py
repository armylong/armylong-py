import os
import logging
from internal.business.coding_agent import save_works
from internal.business.coding_agent import up_feishu_doc

class Main:

    coding_agent_home = "/root/code/coding-agent-testing"  # 正式目录
    coding_agent_workspace = os.path.join(coding_agent_home, "works")

    # run_env = "test"

    # def __init__(self, run_env: str = "test"):
    #     self.run_env = run_env
    #     if self.run_env == "test":
    #         self.coding_agent_home = "/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent"

    # 写入工作目录准备数据
    def save_works(self, record_ids=[]):
        save_works.SaveWorks(self.coding_agent_workspace).main(record_ids=record_ids)

    # 调用ai完成任务
    def call_ai(self):
        pass

    # 将任务结果数据回写至飞书多维表格
    def update_feishu_doc(self, record_ids=[]):
        up_feishu_doc.UpFeishuDoc(self.coding_agent_workspace).main(record_ids=record_ids)
    
    def main(self, record_ids=[]):
        logging.info("从飞书拉取未完成任务数据, 并写入到本地")
        self.save_works(record_ids)

        logging.info("调用ai完成任务, 生成qa_result.json")
        self.call_ai()

        logging.info("将ai处理完的本地数据结果(qa_result.json), 回写至飞书多维表格")
        self.update_feishu_doc()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main = Main()
    logging.info(f"工作目录: {main.coding_agent_workspace}")
    main.main()