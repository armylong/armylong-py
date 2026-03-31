import os
import save_works
import up_feishu_doc

class Main:

    coding_agent_home = "/root/code/coding-agent-testing"  # 正式目录
    coding_agent_workspace = os.path.join(coding_agent_home, "works")

    run_env = "test"

    def __init__(self, run_env: str = "test"):
        self.run_env = run_env
        if self.run_env == "test":
            self.coding_agent_home = "/root/code/stepBYstep/pyCode/armylong-py/internal/business/coding_agent"

    # 写入工作目录准备数据
    def save_works(self):
        save_works.SaveWorks(self.coding_agent_workspace).main()

    def call_ai(self):
        pass

    def update_feishu_doc(self):
        up_feishu_doc.UpFeishuDoc(self.coding_agent_workspace).main()
    
    def main(self):
        # 写入工作目录任务数据
        print("从飞书拉取未完成任务数据, 并写入到本地")
        self.save_works()

        # 调用ai完成任务
        print("\n调用ai完成任务")
        self.call_ai()

        # 将任务结果数据回写至飞书多为表格
        print("\n将任务结果数据回写至飞书多维表格")
        self.update_feishu_doc()
        

if __name__ == "__main__":
    main = Main()
    print(main.coding_agent_workspace)
    main.main()