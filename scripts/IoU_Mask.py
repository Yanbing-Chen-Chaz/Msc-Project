from skimage.measure import label, regionprops
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

pred_path = "C:\\Users\\75695\\Desktop\\image\\testing\\Hela2\\Hela2_8bit_cellposeSAM\\t83xy5c1_seg.npy"
gt_path = "C:\\Users\\75695\\Desktop\\image\\testing\\Hela2\\Hela2_gt\\t83xy5c1_seg.npy"  # 替换为实际的 ground truth 路径
output_path = "C:\\Users\\75695\\Desktop\\iou_overlay.png"

def generate_iou_overlay(gt_path, pred_path, output_path='iou_overlay.png'):
    # 读取数据
    pred_data = np.load(pred_path, allow_pickle=True).item()
    gt_data = np.load(gt_path, allow_pickle=True).item()
    pred_mask = pred_data["masks"]
    gt_mask = gt_data["masks"]

    # 标签化
    gt_labeled = label(gt_mask)
    pred_labeled = label(pred_mask)

    # 创建透明背景图
    height, width = gt_mask.shape
    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim([0, width])
    ax.set_ylim([height, 0])  # 注意 y 轴方向
    ax.axis("off")

    

    # 计算每个 GT 的最大 IOU 并显示在质心位置
    for gt_region in regionprops(gt_labeled):
        gt_id = gt_region.label
        gt_cell_mask = gt_labeled == gt_id
        best_iou = 0

        for pred_region in regionprops(pred_labeled):
            pred_cell_mask = pred_labeled == pred_region.label
            intersection = np.logical_and(gt_cell_mask, pred_cell_mask).sum()
            union = np.logical_or(gt_cell_mask, pred_cell_mask).sum()
            iou = intersection / union if union > 0 else 0
            best_iou = max(best_iou, iou)

        # 获取质心位置
        y, x = gt_region.centroid
        ax.text(x, y, f"{best_iou:.2f}", color="white", fontsize=10, ha="center", va="center")

    # 保存为透明 PNG
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(output_path, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()

    print(f"IOU overlay saved to: {output_path}")

generate_iou_overlay(gt_path, pred_path, output_path)