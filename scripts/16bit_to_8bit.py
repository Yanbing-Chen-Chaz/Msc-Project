import tifffile
import numpy as np
import os

# 输入和输出文件夹路径
input_folder = r'C:\Users\75695\Desktop\image\testing\Hela2\Hela2_gt'      # 修改为你的输入目录
output_folder = r'C:\Users\75695\Desktop\image\testing\Hela2\Hela2_8bit'    # 修改为你的输出目录

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历所有 .tif 或 .tiff 文件
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.tif', '.tiff')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 读取原始图像
        img = tifffile.imread(input_path)

        # 归一化到 0-255 并转换为 8-bit
        img_8bit = ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)

        # 保存为新的 TIF 文件
        tifffile.imwrite(output_path, img_8bit)

        print(f"Processed: {filename}")