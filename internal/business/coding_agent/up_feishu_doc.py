import os
import json
import requests
from datetime import datetime
import feishu_doc_data

class UpFeishuDoc:

    works_dir = ""
    feishu_doc = None

    def __init__(self, works_dir: str):
        if not works_dir or not works_dir.strip():
            raise Exception("works_dir 不能为空")

        if not os.path.exists(works_dir):
            raise Exception(f"works_dir {works_dir} 不存在")
        
        self.works_dir = works_dir
        self.feishu_doc = feishu_doc_data.FeishuDocData()

    def instance_is_complete(self, instance_id: str)->dict:
        """是否是已完成的题目数据"""
        instance_dir = os.path.join(self.works_dir, instance_id)
        if not os.path.exists(instance_dir):
            raise Exception(f"题目目录 {instance_dir} 不存在")
        
        # 检查目录中有没有子目录
        model_dirs = [f"{instance_dir}/{item}" for item in os.listdir(instance_dir) if os.path.isdir(f"{instance_dir}/{item}")]
        if not model_dirs:
            raise Exception(f"题目目录 {instance_dir} 下没有子目录, 请检查是否完成")
        # 只会有一份答案
        if len(model_dirs) != 1:
            raise Exception(f"题目目录 {instance_dir} 下有多个子目录, 请检查是否完成")

        # 答案目录
        result_dir = model_dirs[0]
        
        # 检查子目录下是否有qa_result.json文件
        qa_result_json_path = os.path.join(result_dir, "qa_result.json")
        if not os.path.exists(qa_result_json_path):
            return {}

        # 检查子目录下是否有qa_result.done文件
        qa_result_done_path = os.path.join(result_dir, "qa_result.done")
        if not os.path.exists(qa_result_done_path):
            return {}
        
        # 读取qa_result.json文件内容
        qa_result = {}
        with open(qa_result_json_path, "r", encoding="utf-8") as f:
            qa_result = json.loads(f.read())

        if not qa_result:
            # 走到这一步, 百分之百得有json了
            raise Exception(f"qa_result.json 文件 {qa_result_json_path} 内容为空")

        return qa_result

    def update_feishu_doc(self, record_id: str, row_id: str, model_name: str, model_qa_result: dict):
        ## 获取题目目录下qa_result.md文档数据
        ## 拆分出每个模型数据: 模型名称 | 多个约束的分值 | 不为满分的理由
        ## 调用飞书写入接口写入飞书多维表格
        result = model_qa_result.get("result", "")
        score_list = model_qa_result.get("score_list", [])
        if not score_list:
            raise Exception(f"{row_id}.qa_result.json 文件 {qa_result_json_path} 内容为空")
        
        feishu_up_map = {
            self.feishu_doc.complete_key: self.feishu_doc.complete_value,  # 标记已完成
        }
        if result != "" or result.strip() != "":
            feishu_up_map[self.feishu_doc.not_full_score_reason_key] = result

            
        has_not_full_score_yn = False
        for item in score_list:
            _constraints_id = item.get("constraints_id", 0)
            _score = item.get("score", 0)
            if _constraints_id == 0 or _score == 0 or _score > 3:
                raise Exception(f"{row_id}.qa_result.json 文件中, {model_name} 约束ID或分值为空或f分值大于3")
            if _score != 3:
                has_not_full_score_yn = True
            constraints_content_people_key = self.feishu_doc.constraints_content_people_key.format(_constraints_id)
            feishu_up_map[constraints_content_people_key] = str(_score)

        if has_not_full_score_yn and result == "":
            raise Exception(f"{row_id}.qa_result.json 文件中, {model_name} 不都是满分, 但是没有理由")
        if not has_not_full_score_yn and result != "":
            raise Exception(f"{row_id}.qa_result.json 文件中, {model_name} 全是满分, 但是有理由")

        url = "http://0.0.0.0/feishu/updateBaseTables"
        params = {
            "app_token": "ZFszben8BaPhvPscIbLcmKsZnYB",
            "table_id": "tbluYT98DikJIQp1",
            "record_id": record_id,
            "update_base_tables_url_request_json": {"fields": feishu_up_map}
        }
        print(params)

        response = requests.post(url, json=params).json()
        if response.get("errorCode", -1) != 0:
            raise Exception(response.get("errorMsg", "更新飞书文档失败 go服务报错"))

        doc_response = response.get("responseData", {})
        if doc_response.get("code", -1) != 0:
            raise Exception(doc_response.get("msg", "更新飞书文档失败 飞书接口报错"))

        print(doc_response)

    # 将任务结果数据回写至飞书多为表格
    def main(self, record_ids=[]):
        # 循环查找飞书文档中未完成的任务
        for record in self.feishu_doc.table_records:
            record_id = record.get("record_id", "")
            if not record_id or not record_id.strip():
                raise Exception(f"飞书文档行 {record} 缺少 record_id 字段")
            if len(record_ids) > 0 and record_id not in record_ids:
                continue
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
            if self.feishu_doc.row_is_complete(row) and datetime.now().strftime("%Y%m%d") != "202603312":
                print(f"已完成, 跳过: {record_id}{row_id}:{model_name}")
                continue
            
            print(f"检测到未完成的题目, 开始将数据写入到飞书多维表格中: {record_id}{row_id}:{model_name}")
            # 查找对应目录判断题目是否已完成
            qa_result = self.instance_is_complete(row_id)
            if not qa_result:
                print(f"题目 {record_id}{row_id} 未完成, 跳过")
                continue

            # 因为qa_result.json是多个模型的处理结果(一个模型代表一行, 本次就只处理当前模型的数据)
            model_qa_result = qa_result[model_name]
            if not model_qa_result:
                raise Exception(f"qa_result.json文件中没有对应模型{model_name}的数据")

            self.update_feishu_doc(record_id, row_id, model_name, model_qa_result)


if __name__ == "__main__":
    up_feishu_doc = UpFeishuDoc("/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent/works")
    up_feishu_doc.main(record_ids=["recveSGMtiwwVe"])
