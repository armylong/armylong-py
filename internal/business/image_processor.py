# image_processor.py（增强版本）
import os
from PIL import Image, ImageEnhance, ImageOps
import argparse

class ImageBatchProcessor:
    """基础图片批量处理器：支持缩放、灰度化、增强、格式转换、去阴影"""
    def __init__(self, input_dir, output_dir, process_type=None):
        self.input_dir = input_dir
        self.process_type = process_type
        
        # 自动生成输出目录（如果未指定）
        if not output_dir and process_type:
            input_dir_abs = os.path.abspath(input_dir)
            output_dir = f"{input_dir_abs}_{process_type}"
        
        self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 统计信息
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": []
        }

    def _get_processed_filename(self, original_name, process_type, **kwargs):
        """生成处理后的文件名"""
        name, ext = os.path.splitext(original_name)
        ext = ext.lower()
        
        if process_type == "resize":
            width = kwargs.get("width", 0)
            height = kwargs.get("height", 0)
            return f"{name}_resize_{width}_{height}{ext}"
        elif process_type == "grayscale":
            width = kwargs.get("width", 0)
            height = kwargs.get("height", 0)
            return f"{name}_grayscale_{width}_{height}{ext}"
        elif process_type == "enhance":
            brightness = kwargs.get("brightness", 1.0)
            contrast = kwargs.get("contrast", 1.0)
            return f"{name}_enhance_{brightness:.1f}_{contrast:.1f}{ext}"
        elif process_type == "convert":
            target_format = kwargs.get("target_format", "jpg")
            original_ext = ext.lstrip(".")
            return f"{name}_convert_{original_ext}.{target_format}"
        elif process_type == "remove-shadow":
            return f"{name}_removeshadow{ext}"
        else:
            return f"{name}_{process_type}{ext}"


    def resize_image(self, img_path, target_width=None, target_height=None, scale=None):
        """缩放图片"""
        try:
            img = Image.open(img_path)
            
            original_width, original_height = img.size
            
            # 计算目标尺寸
            if scale is not None:
                # 按比例缩放
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
            elif target_width and target_height:
                # 严格按照指定尺寸缩放（可能拉伸）
                new_width = target_width
                new_height = target_height
            elif target_width:
                # 指定宽度，高度按比例计算
                ratio = target_width / original_width
                new_width = target_width
                new_height = int(original_height * ratio)
            elif target_height:
                # 指定高度，宽度按比例计算
                ratio = target_height / original_height
                new_width = int(original_width * ratio)
                new_height = target_height
            else:
                new_width, new_height = original_width, original_height
            
            # 使用高质量重采样
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img.close()
            return resized_img, new_width, new_height
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 缩放失败：{str(e)}")
            return None, 0, 0

    def grayscale_image(self, img_path):
        """灰度化处理"""
        try:
            img = Image.open(img_path)
            
            gray_img = img.convert("L")
            width, height = img.size
            img.close()
            return gray_img, width, height
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 灰度化失败：{str(e)}")
            return None, 0, 0

    def enhance_image(self, img_path, brightness=1.0, contrast=1.0):
        """亮度和对比度增强"""
        try:
            # 参数验证
            if not (0.1 <= brightness <= 5.0) or not (0.1 <= contrast <= 5.0):
                raise ValueError(f"亮度/对比度值必须在0.1-5.0范围内（当前：亮度={brightness}, 对比度={contrast}）")
            
            img = Image.open(img_path)
            
            # 转换为RGB模式以支持所有图像处理
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            
            # 调整亮度
            if brightness != 1.0:
                brightness_enhancer = ImageEnhance.Brightness(img)
                img = brightness_enhancer.enhance(brightness)
            
            # 调整对比度
            if contrast != 1.0:
                contrast_enhancer = ImageEnhance.Contrast(img)
                img = contrast_enhancer.enhance(contrast)
            
            return img
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 增强失败：{str(e)}")
            return None

    def convert_image(self, img_path, target_format="jpg"):
        """图片格式转换"""
        try:
            img = Image.open(img_path)
            
            # PNG转JPG需要处理透明通道
            if target_format.lower() in ["jpg", "jpeg"]:
                if img.mode in ("RGBA", "LA"):
                    # 创建白色背景
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    # 将alpha通道作为掩码
                    if img.mode == "RGBA":
                        background.paste(img, mask=img.split()[3])
                    else:
                        background.paste(img, mask=img.split()[1])
                    img = background
                elif img.mode != "RGB":
                    # 转换为RGB模式
                    img = img.convert("RGB")
            
            return img
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 格式转换失败：{str(e)}")
            return None

    def remove_shadow(self, img_path):
        """阴影去除与亮度均匀化（使用Pillow简单实现）"""
        try:
            img = Image.open(img_path)
            
            # 转换为RGB模式
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # 分离通道
            r, g, b = img.split()
            
            # 对每个通道进行直方图均衡化
            r_eq = ImageOps.equalize(r)
            g_eq = ImageOps.equalize(g)
            b_eq = ImageOps.equalize(b)
            
            # 合并通道
            eq_img = Image.merge("RGB", (r_eq, g_eq, b_eq))
            
            # 应用轻微的亮度增强
            brightness_enhancer = ImageEnhance.Brightness(eq_img)
            result_img = brightness_enhancer.enhance(1.2)
            
            img.close()
            return result_img
        except Exception as e:
            self.stats["failed"].append(f"{img_path} - 阴影去除失败：{str(e)}")
            return None

    def process(self, process_type, resize_w=800, resize_h=600, scale=None, brightness=1.0, contrast=1.0, target_format="jpg"):
        """批量处理图片"""
        # 支持的图片格式
        supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
        
        # 遍历输入目录
        for filename in os.listdir(self.input_dir):
            self.stats["total"] += 1
            img_path = os.path.join(self.input_dir, filename)
            
            # 仅处理图片文件
            if not filename.lower().endswith(supported_formats):
                self.stats["failed"].append(f"{img_path} - 非图片文件，跳过")
                continue
            
            # 执行处理
            processed_img = None
            new_filename = None
            
            if process_type == "resize":
                processed_img, width, height = self.resize_image(img_path, resize_w, resize_h, scale)
                if processed_img:
                    new_filename = self._get_processed_filename(filename, process_type, width=width, height=height)
            elif process_type == "grayscale":
                processed_img, width, height = self.grayscale_image(img_path)
                if processed_img:
                    new_filename = self._get_processed_filename(filename, process_type, width=width, height=height)
            elif process_type == "enhance":
                processed_img = self.enhance_image(img_path, brightness, contrast)
                if processed_img:
                    new_filename = self._get_processed_filename(filename, process_type, brightness=brightness, contrast=contrast)
            elif process_type == "convert":
                processed_img = self.convert_image(img_path, target_format)
                if processed_img:
                    new_filename = self._get_processed_filename(filename, process_type, target_format=target_format)
                    # 修改扩展名
                    name, _ = os.path.splitext(new_filename)
                    new_filename = f"{name}.{target_format.lower()}"
            elif process_type == "remove-shadow":
                processed_img = self.remove_shadow(img_path)
                if processed_img:
                    new_filename = self._get_processed_filename(filename, process_type)
            else:
                self.stats["failed"].append(f"{img_path} - 不支持的处理类型：{process_type}")
                continue
            
            # 保存处理后的图片
            if processed_img and new_filename:
                save_path = os.path.join(self.output_dir, new_filename)
                # 根据格式选择保存参数
                if new_filename.lower().endswith((".jpg", ".jpeg")):
                    processed_img.save(save_path, quality=95, subsampling=0)
                else:
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