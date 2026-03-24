import click
from business.image_processor import ImageBatchProcessor

@click.command(name='image_processor')
@click.option('--input', '-i', type=str, default='', help='输入目录路径')
@click.option('--output', '-o', type=str, default='', help='输出目录路径')
@click.option('--type', '-t', type=str, default='resize', help='处理类型：resize（缩放）/grayscale（灰度化）')
@click.option('--width', '-w', type=int, default=800, help='缩放目标宽度（仅resize生效）')
@click.option('--height', '-h', type=int, default=600, help='缩放目标高度（仅resize生效）')
def image_processor_handler(input, output, type, width, height):
    """图片批量处理"""
    processor = ImageBatchProcessor(input_dir=input, output_dir=output)
    processor.process(process_type=type, resize_w=width, resize_h=height)
    return processor.stats()
