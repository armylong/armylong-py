# image_processor.py（基础版本）
import os
import time
from PIL import Image, ImageEnhance
import argparse

class ImageBatchProcessor:
    """基础图片批量处理器：支持缩放、灰度化、重命名"""
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        # 统计信息
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": []
        }

    def _get_processed_filename(self, original_name, process_type):
        """生成处理后的文件名：原名称_处理类型_时间戳.后缀"""
        name, ext = os.path.splitext(original_name)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        return f"{name}_{process_type}_{timestamp}{ext}"

    def resize_image(self, img_path, target_width, target_height):
        """缩放图片到指定尺寸"""
        try:
            with Image.open(img_path) as img:
                # 简单缩放（不保持比例）
                resized_img = img.resize((target_width, target_height))
                return resized_img
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 缩放失败：{str(e)}")
            return None

    def grayscale_image(self, img_path):
        """灰度化处理"""
        try:
            with Image.open(img_path) as img:
                gray_img = img.convert("L")
                return gray_img
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 灰度化失败：{str(e)}")
            return None

    def process(self, process_type, resize_w=800, resize_h=600):
        """批量处理图片"""
        # 遍历输入目录
        for filename in os.listdir(self.input_dir):
            self.stats["total"] += 1
            img_path = os.path.join(self.input_dir, filename)
            # 仅处理图片文件
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                self.stats["failed"].append(f"{img_path} - 非图片文件，跳过")
                continue

            # 执行处理
            if process_type == "resize":
                processed_img = self.resize_image(img_path, resize_w, resize_h)
            elif process_type == "grayscale":
                processed_img = self.grayscale_image(img_path)
            else:
                self.stats["failed"].append(f"{img_path} - 不支持的处理类型：{process_type}")
                continue

            # 保存处理后的图片
            if processed_img:
                new_filename = self._get_processed_filename(filename, process_type)
                save_path = os.path.join(self.output_dir, new_filename)
                processed_img.save(save_path)
                self.stats["success"] += 1

        # 输出统计报告
        print("===== 处理报告 =====")
        print(f"总文件数：{self.stats['total']}")
        print(f"成功数：{self.stats['success']}")
        print(f"失败数：{len(self.stats['failed'])}")
        if self.stats["failed"]:
            print("失败详情：")
            for err in self.stats["failed"]:
                print(f"  - {err}")

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="基础图片批量处理工具")
    parser.add_argument("--input", "-i", required=True, help="输入目录路径")
    parser.add_argument("--output", "-o", required=True, help="输出目录路径")
    parser.add_argument("--type", "-t", required=True, choices=["resize", "grayscale"], help="处理类型：resize（缩放）/grayscale（灰度化）")
    parser.add_argument("--width", "-w", type=int, default=800, help="缩放目标宽度（仅resize生效）")
    parser.add_argument("--height", "-h", type=int, default=600, help="缩放目标高度（仅resize生效）")
    
    args = parser.parse_args()
    
    # 初始化并执行处理
    processor = ImageBatchProcessor(args.input, args.output)
    processor.process(args.type, args.width, args.height)