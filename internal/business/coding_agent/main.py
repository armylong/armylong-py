import os
import save_works
import up_feishu_doc

class Main:

    coding_agent_home = "/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent"

    def __init__(self):
        pass

    # 写入工作目录准备数据
    def save_works(self):
        works_dir = os.path.join(self.coding_agent_home, "works")
        save_works.SaveWorks(works_dir).main()

    def call_ai(self):
        pass

    def update_feishu_doc(self):
        works_dir = os.path.join(self.coding_agent_home, "works")
        up_feishu_doc.UpFeishuDoc(works_dir).main()
    
    def main(self):
        # 写入工作目录任务数据
        self.save_works()

        # 调用ai完成任务
        self.call_ai()

        # 将任务结果数据回写至飞书多为表格
        self.update_feishu_doc()
        

if __name__ == "__main__":
    main = Main()
    main.main()