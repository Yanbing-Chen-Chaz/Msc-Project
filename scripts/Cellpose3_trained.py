import numpy as np
from cellpose import models, core, io, plot
from pathlib import Path
from tqdm import trange
from natsort import natsorted


io.logger_setup() # run this to get printing of progress

#Check if colab notebook instance has GPU access

#model = models.Cellpose(model_type='cyto3', gpu=True)
modelpath = r"C:\Users\75695\Desktop\models\cho2_3"
model = models.CellposeModel(pretrained_model=modelpath, gpu=True)
# *** change to your google drive folder path ***
dir = r"C:\Users\75695\Desktop\image\testing\cho2\cho2_cellpose3_t"
dir = Path(dir)
if not dir.exists():
  raise FileNotFoundError("directory does not exist")

# *** change to your image extension ***
image_ext = ".tif"

# list all files
files = natsorted([f for f in dir.glob("*"+image_ext) if "_seg" not in f.name and "_flows" not in f.name])

if(len(files)==0):
  raise FileNotFoundError("no image files found, did you specify the correct folder and extension?")
else:
  print(f"{len(files)} images in folder:")

for f in files:
  print(f.name)

# 假设 img 是 (H, W) 形式的灰度图
flow_threshold = 0.4
cellprob_threshold = 0.0
tile_norm_blocksize = 0

masks_ext = ".png" if image_ext == ".png" else ".tif"

for i in trange(len(files)):
    f = files[i]
    img = io.imread(f)

    # 运行分割模型
    masks, flows, styles = model.eval(
        img,
        diameter=None,
        flow_threshold=flow_threshold,
        cellprob_threshold=cellprob_threshold,
        normalize={"tile_norm_blocksize": tile_norm_blocksize},
        do_3D=False
    )

    # 保存为 GUI 可加载格式（.npy + 可视化）
    file_name = str(f.with_name(f.stem))  # 不带扩展名的完整路径
    io.masks_flows_to_seg(img, masks, flows, file_name, channels=[0, 0])