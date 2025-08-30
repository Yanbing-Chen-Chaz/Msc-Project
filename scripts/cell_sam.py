import imageio.v3 as iio
import numpy as np
from pathlib import Path
from tqdm import trange
from natsort import natsorted
from cellSAM import cellsam_pipeline

def save_cellpose_npy(img, mask, save_path, original_name):
    outlines = (mask > 0).astype(np.uint8)
    data = {
        'masks': mask.astype(np.uint16),
        'outlines': outlines,
        'chan_choose': [0, 0],
        'filename': original_name
    }
    np.save(save_path, data)

def batch_cellsam(input_dir, output_dir, image_ext=".tif"):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not input_dir.exists():
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    files = natsorted([f for f in input_dir.glob(f"*{image_ext}") if "_seg" not in f.stem])
    if len(files) == 0:
        raise FileNotFoundError(f"未找到符合条件的 {image_ext} 文件")

    print(f"共找到 {len(files)} 张图像，开始处理...")

    for i in trange(len(files), desc="Processing images"):
        f = files[i]
        img = iio.imread(f)

        # 运行 cellsam_pipeline 分割
        mask = cellsam_pipeline(img, use_wsi=False, low_contrast_enhancement=False, gauge_cell_size=False)

        save_name = f.stem + "_seg.npy"
        save_path = output_dir / save_name

        save_cellpose_npy(img, mask, save_path, f.name)

    print("所有图像处理完成！")

if __name__ == "__main__":
    input_folder = r"C:\Users\75695\Desktop\image\testing\Hela2\Hela2_cellsam"
    output_folder = r"C:\Users\75695\Desktop\image\testing\Hela2\Hela2_cellsam"
    batch_cellsam(input_folder, output_folder)