import sys
from PIL import Image

def process_image(image_path):
    # 在这里添加你的图像处理逻辑
    with Image.open(image_path) as img:
        # 示例：打印图像的尺寸
        print(f"处理图像: {image_path}, 尺寸: {img.size}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        process_image(image_path)
    else:
        print("错误: 未提供图片路径")
        sys.exit(1) 