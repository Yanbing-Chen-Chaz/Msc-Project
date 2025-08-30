from skimage.measure import label, regionprops
import numpy as np

def evaluate_segmentation(gt_path, pred_path):
    # 从路径读取图像
    pred_data = np.load(pred_path, allow_pickle=True).item()
    gt_data = np.load(gt_path, allow_pickle=True).item()

    # 提取掩码（Cellpose 通常保存在 "masks" 键中）
    pred_mask = pred_data["masks"]
    gt_mask = gt_data["masks"]

    # === 嵌套定义：计算 GT 与预测的最大 IoU ===
    def compute_iou(gt_mask, pred_mask):
        gt_labeled = label(gt_mask)
        pred_labeled = label(pred_mask)
        iou_dict = {}
        for gt_region in regionprops(gt_labeled):
            gt_id = gt_region.label
            gt_cell_mask = gt_labeled == gt_id
            best_iou = 0
            for pred_region in regionprops(pred_labeled):
                pred_id = pred_region.label
                pred_cell_mask = pred_labeled == pred_id
                intersection = np.logical_and(gt_cell_mask, pred_cell_mask).sum()
                union = np.logical_or(gt_cell_mask, pred_cell_mask).sum()
                iou = intersection / union if union > 0 else 0
                best_iou = max(best_iou, iou)
            iou_dict[gt_id] = best_iou
        return iou_dict

    # === 计算每个 GT 对应的最大 IoU ===
    iou_results = compute_iou(gt_mask, pred_mask)

    thresholds = np.arange(0.5, 1.0, 0.05)
    precision_list = []

    pred_labeled = label(pred_mask)
    pred_ids = np.unique(pred_labeled)
    pred_ids = pred_ids[pred_ids != 0]
    gt_labeled = label(gt_mask)

    for thresh in thresholds:
        TP, FP, FN = 0, 0, 0
        matched_pred_ids = set()

        for gt_id, iou in iou_results.items():
            if iou >= thresh:
                TP += 1
            else:
                FN += 1

        for gt_region in regionprops(gt_labeled):
            gt_id = gt_region.label
            gt_cell_mask = gt_labeled == gt_id
            best_iou, matched_pred_id = 0, None
            for pred_region in regionprops(pred_labeled):
                pred_id = pred_region.label
                pred_cell_mask = pred_labeled == pred_id
                intersection = np.logical_and(gt_cell_mask, pred_cell_mask).sum()
                union = np.logical_or(gt_cell_mask, pred_cell_mask).sum()
                iou = intersection / union if union > 0 else 0
                if iou > best_iou:
                    best_iou = iou
                    matched_pred_id = pred_id
            if best_iou >= thresh and matched_pred_id is not None:
                matched_pred_ids.add(matched_pred_id)

        FP = len(pred_ids) - len(matched_pred_ids)
        precision = TP / (TP + FP + FN + 1e-8)
        precision_list.append(precision)

    mean_precision = np.mean(precision_list)
    precision_at_0_5 = precision_list[0]  # 第一个就是 threshold = 0.5 时的值
    return mean_precision, precision_at_0_5  # ❗返回值，主脚本中调用后可用