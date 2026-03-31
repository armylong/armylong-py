import os
import json

class UpFeishuDoc:

    works_dir = ""

    def __init__(self, works_dir: str):
        if not works_dir or not works_dir.strip():
            raise Exception("works_dir 不能为空")

        if not os.path.exists(works_dir):
            raise Exception(f"works_dir {works_dir} 不存在")
        
        self.works_dir = works_dir

    def format_qa_result(self, qa_result_md_path: str)->dict:
        """格式化qa_result"""
        with open(qa_result_md_path, "r", encoding="utf-8") as f:
            qa_result = f.read()

        # 如果判断没有完成, 直接返回空字典
        exit(0)
        return qa_result

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
        
        # 检查子目录下是否有qa_result.md文件
        qa_result_md_path = os.path.join(result_dir, "qa_result.md")
        if not os.path.exists(qa_result_md_path):
            return {}
        
        # 读取qa_result.md文件内容
        qa_result = self.format_qa_result(qa_result_md_path)
        if not qa_result:
            return {}

        return qa_result

    def update_feishu_doc(self, instance_id: str):
        ## 获取题目目录下qa_result.md文档数据
        ## 拆分出每个模型数据: 模型名称 | 多个约束的分值 | 不为满分的理由
        ## 调用飞书写入接口写入飞书多维表格
        qa_result = self.instance_is_complete(instance_id)
        if not qa_result:
            print(f"题目 {instance_id} 未完成, 跳过")
            return

        

        pass

    # 将任务结果数据回写至飞书多为表格
    def main(self):
        # 循环处理工作目录下所有已完成的题目
        # 获取所有子目录
        instance_ids = [item for item in os.listdir(self.works_dir) if os.path.isdir(os.path.join(self.works_dir, item))]

        # 循环处理每个题目
        for instance_id in instance_ids:
            print(f"处理题目 {instance_id}")
            self.update_feishu_doc(instance_id)


if __name__ == "__main__":
    up_feishu_doc = UpFeishuDoc("/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent/works")
    up_feishu_doc.main()
