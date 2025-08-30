import os
import re
import glob
import numpy as np
import pandas as pd
from skimage.io import imread

# === Config ===
data_dir = r"C:\Users\75695\Desktop\Hela2_8"
out_csv = r"C:\Users\75695\Desktop\Hela2_3.csv"

# File collection
mask_files = sorted(glob.glob(os.path.join(data_dir, "*c1_seg.npy")))

def extract_t_from_name(path):
    # Try to match digits after t or T: ..._t12_... or ...T12...
    m = re.search(r'[tT](\d+)', os.path.basename(path))
    return int(m.group(1)) if m else None

per_file_records = []  # Per-file records for later aggregation by t

for mask_file in mask_files:
    image_file = mask_file.replace("c1_seg.npy", "c3.tif")

    # Parse t
    t_val = extract_t_from_name(mask_file)
    if t_val is None:
        print(f"Skipping {mask_file}: cannot extract t")
        continue

    # Read mask
    data = np.load(mask_file, allow_pickle=True)
    if isinstance(data, np.ndarray) and data.shape == ():
        data = data.item()

    if not (isinstance(data, dict) and 'masks' in data):
        print(f"Skipping {mask_file}: unexpected content or missing 'masks'")
        continue
    mask = data['masks']

    # Read image
    try:
        img = imread(image_file)
    except FileNotFoundError:
        print(f"Skipping {mask_file}: image not found {image_file}")
        continue

    if img.ndim == 3:
        img = img[..., 0]

    if mask.shape != img.shape:
        print(f"Skipping {mask_file}: shape mismatch: mask {mask.shape}, image {img.shape}")
        continue

    # Compute total and n_cells for this field of view (this xy)
    region = mask > 0
    total_val = img[region].sum() if np.any(region) else 0
    n_cells = max(len(np.unique(mask)) - 1, 0)  # Exclude background label 0

    per_file_records.append({
        "T": t_val,
        "Mask_File": os.path.basename(mask_file),
        "Image_File": os.path.basename(image_file),
        "Total_Intensity": float(total_val),
        "N_Cells": int(n_cells),
    })

# Exit if no records
if not per_file_records:
    print("No valid files found. Nothing to save.")
else:
    # Aggregate by t: sum multiple xy of the same t
    df_files = pd.DataFrame(per_file_records)
    agg = df_files.groupby("T", as_index=False)[["Total_Intensity", "N_Cells"]].sum()

    # Compute per-cell mean intensity for each t
    agg["Mean_Per_Cell"] = agg.apply(
        lambda r: (r["Total_Intensity"] / r["N_Cells"]) if r["N_Cells"] > 0 else 0.0, axis=1
    )

    # Optional: also compute pixel-level mean (if needed)
    # To do that you would need total pixel counts; skip for now

    # Save
    agg = agg[["T", "Total_Intensity", "N_Cells", "Mean_Per_Cell"]].sort_values("T")
    agg.to_csv(out_csv, index=False)
    print(f"Saved per-t aggregation to: {out_csv}")