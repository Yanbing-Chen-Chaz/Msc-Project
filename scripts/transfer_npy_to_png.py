import os
import numpy as np
import imageio.v2 as imageio
from glob import glob

npy_dir = r"C:\Users\75695\Desktop\cho1_gt"
output_dir = os.path.join(npy_dir, r"C:\Users\75695\Desktop\pngmask")
os.makedirs(output_dir, exist_ok=True)

npy_paths = glob(os.path.join(npy_dir, "*_seg.npy"))

for npy_path in npy_paths:
    data = np.load(npy_path, allow_pickle=True).item()
    mask = data["masks"]
    filename = os.path.basename(npy_path).replace("_seg.npy", "_mask.png")
    save_path = os.path.join(output_dir, filename)
    imageio.imwrite(save_path, mask.astype(np.uint16))
    print(f"[✓] {filename} saved.")


