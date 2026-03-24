import os
import importlib
import click
from pathlib import Path

# 根命令（对应Go的RootCmd）
@click.group()
@click.option('--toggle', '-t', is_flag=True, help='Help message for toggle')
def root_cmd(toggle):
    pass

# ========== 自动遍历cmd目录注册命令 ==========
def register_all_commands():
    # cmd目录路径
    cmd_dir = Path(__file__).parent / "cmd"
    # 遍历所有.py文件（排除__init__.py和_开头）
    for file in cmd_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue
        # 模块名：internal.cmd.xxx
        module_name = f"internal.cmd.{file.stem}"
        try:
            # 动态导入模块
            module = importlib.import_module(module_name)
            # 遍历模块成员，找到所有click.Command对象
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, click.Command):
                    # 注册到根命令
                    root_cmd.add_command(attr)
        except Exception as e:
            click.echo(f"加载 {module_name} 失败: {e}", err=True)

# 执行注册
register_all_commands()

# 执行入口（对应Go的Execute()）
def execute():
    try:
        root_cmd()
    except Exception as e:
        click.echo(f"命令执行失败: {e}", err=True)
        exit(1)