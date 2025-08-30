import os
from glob import glob
import pandas as pd
from accuracy_calculator import evaluate_segmentation  # 引入你的评估函数（确保 evaluate.py 在同一目录或已在 PYTHONPATH）

# === 设置 GT 和预测结果的文件夹路径 ===
gt_dir = r"C:\Users\75695\Desktop\image\testing\cho\cho_gt"
pred_dir = r"C:\Users\75695\Desktop\image\testing\cho\cho_1915"

# === 获取所有真实标签图像的路径（假设都是 _seg.npy 结尾） ===
gt_paths = sorted(glob(os.path.join(gt_dir, "*_seg.npy")))

# 用于保存每张图像的评估结果
results = []

# === 批量处理每一对图像 ===
for gt_path in gt_paths:
    # 获取文件名核心部分，例如 't000002xy1c1'
    filename_core = os.path.basename(gt_path).replace("_seg.npy", "")

    # 构造预测图像路径
    pred_path = os.path.join(pred_dir, f"{filename_core}_seg.npy")

    # 如果预测图像不存在，跳过该图像
    if not os.path.exists(pred_path):
        print(f"[跳过] 找不到预测图像：{pred_path}")
        continue

    # 调用评估函数，计算平均分割精度
    try:
        mean_score, score_0_5 = evaluate_segmentation(gt_path, pred_path)
    except Exception as e:
        print(f"[错误] 处理失败：{filename_core}，错误信息：{e}")
        continue

    # 保存当前结果
    results.append({
    "图像": filename_core,
    "平均分割精度": round(mean_score, 4),
    "0.5阈值精度": round(score_0_5, 4)
})

    print(f"[完成] {filename_core} -> 精度：{mean_score:.4f}")

# === 转换为 DataFrame 并保存 CSV ===
df = pd.DataFrame(results)
output_path = r"C:\Users\75695\Desktop\image\testing\cho\cho_1915\cho_1915.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n✅ 所有图像处理完成，结果已保存到：{output_path}")