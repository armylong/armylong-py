import sys
import logging
logging.basicConfig(
    level=logging.INFO,          # 允许输出的最小日志级别 DEBUG INFO WARNING ERROR CRITICAL FATAL
    format="%(asctime)s [%(levelname)s] - %(message)s\t# %(filename)s.%(funcName)s():%(lineno)d",  # 日志格式 #  %(asctime)s 时间  %(levelname)s 日志级别（INFO/WARNING/ERROR） %(message)s 你写的日志内容  %(filename)s 文件名（例如 main.py）  %(lineno)d 行号  %(funcName)s 函数名  %(module)s 模块名  %(process)d 进程ID  %(thread)d 线程ID  %(name)s logger名字
    datefmt="%Y-%m-%d %H:%M:%S",               # 时间格式
    stream=sys.stderr,                 # 输出到控制台 sys.stderr(默认) sys.stdout（和 filename 二选一）
    # filename="app.log",          # 输出到文件 app.log （和 stream 二选一）
    # filemode="a",                # 文件写入模式
)
from internal import register_cmd

if __name__ == "__main__":
    register_cmd.execute()
