from business.image_processor import ImageBatchProcessor

def image_processor_handler(**kwargs):
    #     parser = argparse.ArgumentParser(description="基础图片批量处理工具")
    # parser.add_argument("--input", "-i", required=True, help="输入目录路径")
    # parser.add_argument("--output", "-o", required=True, help="输出目录路径")
    # parser.add_argument("--type", "-t", required=True, choices=["resize", "grayscale"], help="处理类型：resize（缩放）/grayscale（灰度化）")
    # parser.add_argument("--width", "-w", type=int, default=800, help="缩放目标宽度（仅resize生效）")
    # parser.add_argument("--height", "-h", type=int, default=600, help="缩放目标高度（仅resize生效）")
    """图片批量处理"""
    processor = ImageBatchProcessor(input_dir=kwargs["input"], output_dir=kwargs["output"])
    processor.process(process_type=kwargs["type"], resize_w=kwargs["width"], resize_h=kwargs["height"])
    return processor.stats