# 1. imports
import sys
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import argparse

# 2. scan_images()
def scan_images(folder, exts=(".jpg", ".png", ".bmp")):
    p = Path(folder)
    if not p.exists():
        raise FileNotFoundError(f"文件夹不存在：{folder}")
    if not p.is_dir():
        raise NotADirectoryError(f"路径不是文件夹：{folder}")
    img_path = []
    for file in p.rglob("*"):
        if file.is_file() and file.suffix.lower() in exts:
            img_path.append(file)
    img_path.sort()
    return img_path

# 3. classify_by_prefix()
def classify_by_prefix(paths):
    res = {}
    for p in paths:
        prefix = p.stem.split("_", 1)[0]
        if prefix not in res:
            res[prefix] = []
        res[prefix].append(p)
    return res

# 4. classify_by_size()
def classify_by_size(paths):
    out = {"small": [], "medium": [], "large": []}
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        h, w = img.shape[:2]
        m = min(h, w)
        if m < 256:
            out["small"].append(p)
        elif m < 512:
            out["medium"].append(p)
        else:
            out["large"].append(p)
    return out

# 5. safe_rename()
def safe_rename(old: Path, new: Path):
    if new.exists():
        raise FileExistsError(f"目标文件已存在：{new}")
    old.rename(new)

# 6. batch_rename()
def batch_rename(paths, prefix="img"):
    plan = []
    for i, p in enumerate(paths, start=1):
        new_name = f"{prefix}_{i:04d}{p.suffix}"
        new_p = p.with_name(new_name)
        plan.append((p, new_p))
    targets = [np for _, np in plan]
    if len(set(targets)) != len(targets):
        raise ValueError("新名字存在重复！")
    for _, new in plan:
        if new.exists():
            raise FileExistsError(f"目标已存在：{new}")
    mapping = {}
    for old, new in plan:
        safe_rename(old, new)
        mapping[old] = new
    return mapping

# 7. build_report()
def build_report(paths, mapping=None, out_csv="report.csv"):
    rows = []
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        old_name, new_name = "", ""
        if mapping is not None:
            for old, new in mapping.items():
                if p == new:
                    old_name = old.name
                    new_name = new.name
                    break
        H, W = img.shape[:2]
        m = min(H, W)
        size_class = "small" if m < 256 else ("medium" if m < 512 else "large")
        prefix_class = p.stem.split("_",1)[0]
        rows.append({
            "old_name": old_name,
            "new_name": new_name,
            "path": str(p),
            "width": W,
            "height": H,
            "size_class": size_class,
            "prefix_class": prefix_class
        })
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    return df

# 8. main()
def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    do_rename = "--rename" in sys.argv
    try:
        paths = scan_images(folder)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"❌ {e}")
        return 1

    mapping = None
    if do_rename:
        try:
            mapping = batch_rename(paths, prefix="photo")
            # 👉 就是这里新增一行！
            paths = scan_images(folder)
        except FileExistsError as e:
            print(f"❌ 重命名冲突：{e}")
            return 2
        except ValueError as e:
            print(f"❌ 新名字重复：{e}")
            return 2

    try:
        build_report(paths, mapping, out_csv="report.csv")
    except OSError as e:
        print(f"❌ CSV写入权限错误：{e}")
        return 3

    print("✅ 执行完成")
    return 0

# 9. 入口
if __name__ == "__main__":
    sys.exit(main())
