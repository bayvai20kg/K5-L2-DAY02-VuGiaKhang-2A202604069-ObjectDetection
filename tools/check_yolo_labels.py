#!/usr/bin/env python3
"""Validate YOLO labels before the instructor releases the gold labels."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


VALID_CLASS_IDS = {0, 1, 2, 3}


def image_stems(image_dir: Path) -> set[str]:
    return {path.stem for extension in ("*.jpg", "*.jpeg", "*.png") for path in image_dir.glob(extension)}


def validate_label_file(path: Path) -> list[str]:
    errors = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        parts = line.split()
        if len(parts) != 5:
            errors.append(f"{path.name}:{line_number}: cần đúng 5 giá trị")
            continue
        try:
            class_id = int(parts[0])
            values = [float(value) for value in parts[1:]]
        except ValueError:
            errors.append(f"{path.name}:{line_number}: class_id phải là số nguyên, tọa độ phải là số")
            continue
        x_center, y_center, width, height = values
        if class_id not in VALID_CLASS_IDS:
            errors.append(f"{path.name}:{line_number}: class_id phải thuộc {sorted(VALID_CLASS_IDS)}")
        if not all(0 <= value <= 1 for value in values) or width <= 0 or height <= 0:
            errors.append(f"{path.name}:{line_number}: tọa độ normalized phải nằm trong [0, 1], width/height > 0")
        epsilon = 1e-6
        if x_center - width / 2 < -epsilon or x_center + width / 2 > 1 + epsilon or y_center - height / 2 < -epsilon or y_center + height / 2 > 1 + epsilon:
            errors.append(f"{path.name}:{line_number}: box vượt ngoài biên ảnh")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra cấu trúc nhãn YOLO của 50 ảnh train.")
    parser.add_argument("--images", type=Path, default=Path("dataset/images/train"))
    parser.add_argument("--labels", type=Path, default=Path("dataset/labels/train"))
    args = parser.parse_args()

    expected = image_stems(args.images)
    if not expected:
        errors = [f"Không tìm thấy ảnh trong {args.images}"]
    else:
        errors = []
    actual = {path.stem for path in args.labels.glob("*.txt")}
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        errors.append(f"Thiếu {len(missing)} file nhãn: {', '.join(missing[:8])}{' ...' if len(missing) > 8 else ''}")
    if unexpected:
        errors.append(f"Có {len(unexpected)} file nhãn không có ảnh tương ứng: {', '.join(unexpected[:8])}")
    for label in sorted(args.labels.glob("*.txt")):
        errors.extend(validate_label_file(label))

    if errors:
        print("KHÔNG ĐẠT - hãy sửa các lỗi sau:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"ĐẠT cấu trúc: {len(actual)}/{len(expected)} file nhãn hợp lệ. Chờ ground truth để chấm chất lượng.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
