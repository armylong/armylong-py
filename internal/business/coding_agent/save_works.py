import os
import json
import feishu_doc_data


class SaveWorks:
    
    works_dir = ""
    feishu_doc = None

    def __init__(self, works_dir: str):
        if not works_dir or not works_dir.strip():
            raise Exception("works_dir 不能为空")

        if not os.path.exists(works_dir):
            raise Exception(f"works_dir {works_dir} 不存在")
        
        self.works_dir = works_dir
        self.feishu_doc = feishu_doc_data.FeishuDocData()

    def save_json(self, row_id: str, model_name: str, json_data: dict):
        if not json_data:
            raise Exception(f"飞书文档行 {row_id} 缺少 {self.feishu_doc.json_key} 列")
        json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
        if not json_str or not json_str.strip():
            raise Exception(f"飞书文档行 {row_id} json数据异常 为空")
        with open(f"{self.works_dir}/{row_id}/{model_name}.json", "w", encoding="utf-8") as f:
            f.write(json_str)

    def save_prompt_md(self, row_id: str, model_name: str, prompt_str: str):
        if not prompt_str or not prompt_str.strip():
            raise Exception(f"飞书文档行 {row_id} 提示词数据异常 为空")
        with open(f"{self.works_dir}/{row_id}/prompt.md", "w", encoding="utf-8") as f:
            f.write(prompt_str)
        
        
       
    def main(self):
        for record in self.feishu_doc.table_records:
            record_id = record.get("record_id", "")
            if not record_id or not record_id.strip():
                raise Exception(f"飞书文档行 {record} 缺少 record_id 字段")
            row = record.get("record_data", {})
            if not row:
                raise Exception(f"飞书文档行 {record} 缺少 fields 字段")
            row_id = row.get("id", "")
            if not row_id or not row_id.strip():
                raise Exception(f"飞书文档行 {row_id} 缺少ID")
            
            model_name = row.get(self.feishu_doc.model_name_key, "")
            if not model_name or not model_name.strip():
                raise Exception(f"飞书文档行 {row_id} 缺少大模型名称")

            # 已完成的数据就忽略了
            if self.feishu_doc.row_is_complete(row):
                print(f"已完成, 跳过: {row_id}:{model_name}")
                continue
            
            print(f"检测到未完成的题目, 开始写入工作目录: {row_id}:{model_name}")
            # 创建id工作目录(如果存在, 则不创建)
            row_dir = f"{self.works_dir}/{row_id}"
            if not os.path.exists(row_dir):
                os.makedirs(row_dir)
            # 保存提示词
            self.save_prompt_md(row_id, model_name, row.get(self.feishu_doc.prompt_key, ""))
            # 保存json
            self.save_json(row_id, model_name, row.get(self.feishu_doc.json_key, {}))

            
            


if __name__ == "__main__":
    save_json = SaveWorks("/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent/works")
    save_json.main()