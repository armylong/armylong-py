import click
from internal.business.image_processor import ImageBatchProcessor

@click.command(name='image_processor')
@click.option('--input', '-i', type=str, default='', help='输入目录路径')
@click.option('--output', '-o', type=str, default='', help='输出目录路径（未指定则自动生成）')
@click.option('--type', '-t', type=str, default='resize', help='处理类型：resize（缩放）/grayscale（灰度化）/enhance（增强）/convert（转换）/remove-shadow（去阴影）')
@click.option('--width', '-w', type=int, default=800, help='缩放目标宽度（仅resize生效）')
@click.option('--height', '-H', type=int, default=600, help='缩放目标高度（仅resize生效）')
@click.option('--scale', '-s', type=float, default=None, help='缩放比例（优先级高于width/height，仅resize生效，如0.5表示缩放到50%）')
@click.option('--brightness', '-b', type=float, default=1.0, help='亮度值（仅enhance生效，范围0.1-5.0，默认1.0）')
@click.option('--contrast', '-c', type=float, default=1.0, help='对比度值（仅enhance生效，范围0.1-5.0，默认1.0）')
@click.option('--target-format', '-f', type=str, default='jpg', help='目标格式（仅convert生效，可选jpg/png）')
def image_processor_handler(input, output, type, width, height, scale, brightness, contrast, target_format):
    """图片批量处理"""
    processor = ImageBatchProcessor(input_dir=input, output_dir=output, process_type=type)
    processor.process(
        process_type=type,
        resize_w=width,
        resize_h=height,
        scale=scale,
        brightness=brightness,
        contrast=contrast,
        target_format=target_format
    )
    return processor.stats
