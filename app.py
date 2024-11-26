import base64
from flask import Flask, request, jsonify
from gcode import image_to_binary_matrix, optimize_path, generate_gcode
from PIL import Image
import io



app = Flask(__name__)

# # 创建保存图片的文件夹
IMAGE_DIR = "processed_images"
# os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # 获取请求数据
        data = request.get_json()
        image_data = data.get('imageData')
        timestamp = data.get('timestamp')

        if not image_data or not timestamp:
            return jsonify({"error": "缺少必要参数"}), 400
        

        # 将 base64 编码的图像数据转换为图像文件
        image_data_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_data_bytes))
        image_path = f"processed_images/image-{timestamp}.png"
        image.save(image_path)

        # 直接使用提供的图像路径
        # 调用 gcode.py 中的函数处理图像并生成 G-code
        binary_matrix = image_to_binary_matrix(image_path)
        optimized_path = optimize_path(binary_matrix)
        gcode_filename = f"gcode-{timestamp}.gcode"
        generate_gcode(optimized_path, file_name=gcode_filename)


        # 返回 G-code 文件路径
        processed_result = {
            "message": "G-code 已生成并保存",
            "gcode_path": gcode_filename
        }

        return jsonify(processed_result), 200

    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        return jsonify({"error": "处理图片时发生错误"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
