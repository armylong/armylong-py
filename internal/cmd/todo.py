def todo_handler(**kwargs):
    """todo命令核心逻辑：仅读取参数 + 处理业务"""
    # 方式1：通过kwargs直接获取参数（更简洁）
    task_type = kwargs.get('task_type')
    task_id = kwargs.get('task_id')
    title = kwargs.get('title')
    desc = kwargs.get('desc')
    sort = kwargs.get('sort')
    expire_at = kwargs.get('expire_at')

    # 方式2：也可以通过ctx获取（和之前一致）
    # params = ctx.params
    # task_type = params['task_type']

    # 纯业务逻辑（无任何click相关代码）
    if task_type == 'get':
        if task_id == 0:
            print("错误: get命令需要指定 --task_id")
            return
        print(f"✅ 获取任务 {task_id} 详情：标题=测试任务，状态=未完成")
    
    elif task_type == 'create':
        if not title or not desc:
            print("错误: create命令需要指定 --title 和 --desc")
            return
        print(f"✅ 任务创建成功：标题={title}，描述={desc}，排序={sort}")
    
    elif task_type == 'sort':
        if task_id == 0:
            print("错误: sort命令需要指定 --task_id")
            return
        print(f"✅ 任务 {task_id} 排序值已更新为 {sort}")
    
    elif task_type == 'complete':
        if task_id == 0:
            print("错误: complete命令需要指定 --task_id")
            return
        print(f"✅ 任务 {task_id} 已标记为完成")
    
    elif task_type == 'expire':
        print("✅ 检测到 2 个过期任务并已标记")
    
    else:
        print(f"未知命令: {task_type}")
        print("可用命令: get, create, sort, complete, expire")