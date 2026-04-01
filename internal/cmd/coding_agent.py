import click
import logging
from internal.business.coding_agent.main import Main

@click.command(name='coding_agent')
@click.argument('action')
@click.option('--record_ids', type=str, default='', help='记录ID列表（可选，逗号分隔）')
def coding_agent_handler(action, record_ids):   
    """coding_agent命令核心逻辑：仅读取参数 + 处理业务"""
    logging.info("coding_agent命令核心逻辑")
    logging.info(f"action: {action}")
    logging.info(f"record_ids: {record_ids}")
    if action == "":
        logging.error("请输入任务类型")
        return

    main = Main()
    if record_ids:
        record_ids = record_ids.split(",")
    else:
        record_ids = []

    if action == "save_works":
        logging.info("save_works")
        main.save_works(record_ids=record_ids)
    elif action == "update_feishu_doc":
        logging.info("update_feishu_doc")
        main.update_feishu_doc(record_ids=record_ids)
    else:
        logging.error(f"不支持的任务类型: {action}")
   
    return