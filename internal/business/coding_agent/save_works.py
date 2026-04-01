import os
import json
import logging
from internal.business.coding_agent import feishu_doc_data


class SaveWorks:
    
    coding_agent_workspace = ""
    feishu_doc = None

    def __init__(self, coding_agent_workspace: str):
        if not coding_agent_workspace or not coding_agent_workspace.strip():
            raise Exception("coding_agent_workspace 不能为空")

        if not os.path.exists(coding_agent_workspace):
            raise Exception(f"coding_agent_workspace {coding_agent_workspace} 不存在")
        
        self.coding_agent_workspace = coding_agent_workspace
        self.feishu_doc = feishu_doc_data.FeishuDocData()

    def save_json(self, row_id: str, model_name: str, json_data: dict):
        if not json_data:
            raise Exception(f"飞书文档行 {row_id} 缺少 {self.feishu_doc.json_key} 列")
        json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
        if not json_str or not json_str.strip():
            raise Exception(f"飞书文档行 {row_id} json数据异常 为空")
        with open(f"{self.coding_agent_workspace}/{row_id}/{model_name}.json", "w", encoding="utf-8") as f:
            f.write(json_str)
        logging.info(f"写入json完成: {row_id} {model_name}.json")

    def save_prompt_md(self, row_id: str, model_name: str, prompt_str: str):
        if not prompt_str or not prompt_str.strip():
            raise Exception(f"飞书文档行 {row_id} 提示词数据异常 为空")
        with open(f"{self.coding_agent_workspace}/{row_id}/prompt.md", "w", encoding="utf-8") as f:
            f.write(prompt_str)
        logging.info(f"写入提示词完成: {row_id} prompt.md")
        
    # 将飞书文档中未完成的任务, 写入到本地目录中(------已经写入过的直接跳过------)
    def main(self, record_ids=[]):
        if len(record_ids) > 0:
            logging.info(f"只拉取记录ID为 {record_ids} 的未完成任务")
        else:
            logging.info("拉取所有未完成任务")
            
        if len(self.feishu_doc.table_records) == 0:
            logging.info("飞书上没有未完成的任务了")
        
        for record in self.feishu_doc.table_records:
            record_id = record.get("record_id", "")
            if not record_id or not record_id.strip():
                raise Exception(f"飞书文档行 {record} 缺少 record_id 字段")
            if len(record_ids) > 0 and record_id not in record_ids:
                continue
            row = record.get("record_data", {})
            if not row:
                raise Exception(f"飞书文档行 {record} 缺少 fields 字段")
            row_id = row.get(self.feishu_doc.row_id_key, "")
            if not row_id or not row_id.strip():
                raise Exception(f"飞书文档行 {row_id} 缺少ID")
            
            model_name = row.get(self.feishu_doc.model_name_key, "")
            if not model_name or not model_name.strip():
                raise Exception(f"飞书文档行 {row_id} 缺少大模型名称")

            # 已完成的数据就忽略了
            if self.feishu_doc.row_is_complete(row):
                logging.debug(f"已完成, 跳过: {record_id}{row_id}:{model_name}")
                continue
            
            logging.info(f"检测到未完成的题目, 开始写入工作目录: {row_id}:{model_name}")
            # 创建id工作目录(如果存在, 则跳过不重复建)
            row_dir = f"{self.coding_agent_workspace}/{row_id}"
            if not os.path.exists(row_dir):
                logging.info(f"检测到目录不存在, 创建目录 {row_id}")
                os.makedirs(row_dir)
            else:
                logging.info(f"目录已存在, 跳过: {row_dir}")
                continue
            # 保存提示词
            self.save_prompt_md(row_id, model_name, row.get(self.feishu_doc.prompt_key, ""))
            # 保存json
            self.save_json(row_id, model_name, row.get(self.feishu_doc.json_key, {}))

            
            


if __name__ == "__main__":
    save_json = SaveWorks("/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent/works")
    save_json.main(record_ids=["recveSGMtiwwVe"])