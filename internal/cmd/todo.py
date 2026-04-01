import click
import logging

@click.command(name='todo')
@click.argument('task_type')
@click.option('--task_id', '-id', type=int, default=0, help='任务ID（可选）')
@click.option('--title', '-t', type=str, default='', help='任务标题（create时必填）')
@click.option('--desc', '-d', type=str, default='', help='任务描述（create时必填）')
@click.option('--sort', '-s', type=int, default=0, help='任务排序值，数字越大越靠前（可选）')
@click.option('--expire_at', '-e', type=str, default='', help='过期时间，格式：2026-03-23 20:00:00（可选）')
def todo_handler(task_type, task_id, title, desc, sort, expire_at):
    """todo命令核心逻辑：仅读取参数 + 处理业务"""

    if task_type == 'get':
        if task_id == 0:
            logging.error("get命令需要指定 --task_id")
            return
        logging.info(f"获取任务 {task_id} 详情：标题=测试任务，状态=未完成")
    
    elif task_type == 'create':
        if not title or not desc:
            logging.error("create命令需要指定 --title 和 --desc")
            return
        logging.info(f"任务创建成功：标题={title}，描述={desc}，排序={sort}")
    
    elif task_type == 'sort':
        if task_id == 0:
            logging.error("sort命令需要指定 --task_id")
            return
        logging.info(f"任务 {task_id} 排序值已更新为 {sort}")
    
    elif task_type == 'complete':
        if task_id == 0:
            logging.error("complete命令需要指定 --task_id")
            return
        logging.info(f"任务 {task_id} 已标记为完成")
    
    elif task_type == 'expire':
        logging.info("检测到 2 个过期任务并已标记")
    
    else:
        logging.error(f"未知命令: {task_type}")
        logging.info("可用命令: get, create, sort, complete, expire")