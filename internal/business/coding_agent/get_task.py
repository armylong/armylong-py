import os
import logging
from internal.business.coding_agent import feishu_doc_data


class GetTask:
    
    coding_agent_workspace = ""
    feishu_doc = None

    def __init__(self, coding_agent_workspace: str):
        if not coding_agent_workspace or not coding_agent_workspace.strip():
            raise Exception("coding_agent_workspace 不能为空")

        if not os.path.exists(coding_agent_workspace):
            raise Exception(f"coding_agent_workspace {coding_agent_workspace} 不存在")
        
        self.coding_agent_workspace = coding_agent_workspace
        self.feishu_doc = feishu_doc_data.FeishuDocData(filter_and=[{"field_name": self.recipient_key, "operator": "isEmpty", "value": []}])


    def main(self):
        """获取未完成的任务"""
        if len(self.feishu_doc_data.table_records) == 0:
            logging.info("飞书上没有未完成的任务了")
        else:
            logging.info(f"飞书上有 {len(self.feishu_doc_data.table_records)} 条未完成的任务")


if __name__ == "__main__":
    get_task = GetTask(feishu_doc_data)
    get_task.main()