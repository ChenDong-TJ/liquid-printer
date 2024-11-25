from PIL import Image
from datetime import datetime
import numpy as np


def image_to_binary_matrix(image_path, matrix_size=20, threshold=127):
    """
    将输入图像转换为二进制矩阵
    image_path: 输入图像的文件路径
    matrix_size: 输出矩阵的大小（默认为20x20）
    threshold: 二值化的阈值，低于该亮度的像素将视为1，低于该值视为1
    """

    
    # 打开图像并转换为灰度图
    img = Image.open(image_path)
    print(img.mode)
    img=img.convert('RGB').convert('L')  # 先转换为 RGB，再转换为灰度图,不然透明通道可能有问题
  # 'L'模式为灰度模式
    img.show()
    # 调整图像大小为指定的矩阵大小
    # img = img.resize((matrix_size, matrix_size))
    img=img.resize([matrix_size,matrix_size],Image.Resampling.NEAREST)#插值法保像素。。。
    img.show()

    # 初始化二进制矩阵
    binary_matrix = []

    # 遍历图像的每个像素点，应用二值化
    for y in range(matrix_size):
        row = []
        for x in range(matrix_size):
            # 获取像素值
            pixel_value = img.getpixel((x, y))
            print(img.getpixel((x, y)))
            # 二值化处理，基于阈值
            if pixel_value < threshold:
                row.append(1)  # 黑色区域视为1
            else:
                row.append(0)  # 白色区域视为0
        binary_matrix.append(row)
    
    return binary_matrix

def optimize_path(matrix):
    """
    提取所有有效点（像素为1）并生成优化路径。
    """
    # 提取所有有效像素点 (y, x)
    points = [(y, x) for y, row in enumerate(matrix) for x, val in enumerate(row) if val == 1]
    
    # 最近邻算法。
    points = np.array(points)
    n = len(points)
    visited = [False] * n
    path = []

    # 从第一个点开始，
    current_index = 0
    path.append(tuple(points[current_index]))
    visited[current_index] = True

    for _ in range(1, n):
        # 计算当前点到所有未访问点的距离
        distances = np.linalg.norm(points - points[current_index], axis=1)
        distances[visited] = np.inf  # 已访问点置为无穷大

        # 找到最近的点
        next_index = np.argmin(distances)
        path.append(tuple(points[next_index]))
        visited[next_index] = True
        #已经访问过的
        current_index = next_index

    return path
    
def generate_gcode(optimized_path, spacing=2, extrusion_amount=1, file_name="output.gcode"):
    """
    根据优化后的路径生成 G-code。
    """
    full_file_path = f"/processed_images/{file_name}"
    with open(full_file_path, 'w') as f:
        # G-code 初始化
       
        f.write("G21\n")
        f.write("G90 \n")
        f.write("M83\n")
        f.write("G92 E0\n")
        f.write("M107 ; close fan\n")
        f.write("G28 ; set all axes to zero\n")
        f.write("M302 S0\n")
        
        # 起始高度
        Z_ori = 120
        X_ori = 60
        Y_ori = 200
        Z_pos = 70
        mov_speed = 100
        extr_speed = 100
        stop_time = 2500

        # 移动到初始位置
        f.write(f"G1 Z{Z_ori} F5000 \n")
        f.write(f"G1 X{X_ori} Y{Y_ori} F5000 \n")
        f.write(f"G1 Z{Z_pos} F5000 \n")

        # 遍历优化后的路径
        for y, x in optimized_path:
            x_pos = x * spacing + X_ori
            y_pos = Y_ori - y * spacing

            # 移动到点位置
            f.write(f"G1 X{x_pos} Y{y_pos} Z{Z_pos} F{mov_speed}\n")
            
            # 挤出液体
            f.write(f"G1 E{extrusion_amount} F{extr_speed}\n")
            f.write(f"G4 P{stop_time}; stop {stop_time}ms\n")

        # 结束设置
        f.write("G1 Z150 F1000 \n")
        f.write("M107 \n")
        f.write("G28 X0 Y0 ; 只归零X和Y轴，Z轴不变\n")
        f.write("M84 \n")
        f.write("M30 \n")



# mat=image_to_binary_matrix("processed_images/test.png",20,200)


# row_pattern = [1] * 5 + [0] * 5 + [1] * 5 + [0] * 5

# # 使用列表生成式创建 20x20 的矩阵，每行都重复 row_pattern
# test_matrix = [row_pattern for _ in range(20)]

# matrix_np = np.array(mat) * 255
# img = Image.fromarray(matrix_np.astype('uint8'))
# img.show()
# # 调用函数生成G-code
# current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename=f"dots_output{current_time}.gcode"

# generate_gcode(optimize_path(mat), spacing=5, extrusion_amount=100, file_name=filename)



# # 打印结果矩阵(debug用)
# for row in mat:
#     print(row)


