import click
from internal.cmd import todo

# 定义根命令（对应Go的RootCmd）
@click.group()
@click.option('--toggle', '-t', is_flag=True, help='Help message for toggle')
def root_cmd(toggle):
    pass


# 执行入口（对应Go的Execute()）
def execute():
    try:
        root_cmd()
    except Exception as e:
        click.echo(f"命令执行失败: {e}", err=True)
        exit(1)

root_cmd.add_command(click.Command(name='todo',short_help='任务管理',callback=todo.todo_handler,params=[
        click.Argument(param_decls=['task_type'], type=str,required=True),
        click.Option(param_decls=['--task_id', '-id'],type=int,default=0,help='任务ID（可选）'),
        click.Option(param_decls=['--title', '-t'],type=str,default='',help='任务标题（create时必填）'),
        click.Option(param_decls=['--desc', '-d'],type=str,default='',help='任务描述（create时必填）'),
        click.Option(param_decls=['--sort', '-s'],type=int,default=0,help='任务排序值，数字越大越靠前（可选）'),
        click.Option(param_decls=['--expire_at', '-e'],type=str,default='',help='过期时间，格式：2026-03-23 20:00:00（可选）')
    ]))