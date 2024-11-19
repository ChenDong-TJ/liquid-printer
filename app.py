from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime

app = Flask(__name__)

# 创建保存图片的文件夹
IMAGE_DIR = "processed_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # 获取请求数据
        data = request.get_json()
        image_data = data.get('imageData')
        timestamp = data.get('timestamp')

        if not image_data or not timestamp:
            return jsonify({"error": "缺少必要参数"}), 400

        # 将 base64 数据解码为二进制数据
        image_binary = base64.b64decode(image_data)

        # 保存图片到文件
        filename = f"{IMAGE_DIR}/pixel-art-{timestamp}.png"
        with open(filename, 'wb') as image_file:
            image_file.write(image_binary)

        # 在这里对图片进行进一步处理（示例：返回文件路径）
        processed_result = {"message": "图片已处理并保存", "path": filename}

        return jsonify(processed_result), 200

    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        return jsonify({"error": "处理图片时发生错误"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
