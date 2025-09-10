import os
import sys
import gc
import torch

# MUST set custom path BEFORE any ultralytics import
CUSTOM_ULTRA_ROOT = "/media/a/f689f84c-a402-4877-ad42-2c66aa8c80b5/AI-CHAMPION_KBS/DIA-YOLO All file/Ultralytics Folder"
sys.path.insert(0, CUSTOM_ULTRA_ROOT)

# Clean any existing ultralytics imports
for module in list(sys.modules.keys()):
    if module.startswith('ultralytics'):
        del sys.modules[module]

import cv2
import numpy as np
import math
import argparse

# NOW import ultralytics from custom path
import ultralytics
print("✅ Using ultralytics from:", ultralytics.__file__)

from ultralytics import YOLO

# [PCB]
# python test-original.py --weight /home/a/Desktop/Vision/KTJ/BEFORE/학위논문/code/runs/obb/attention-768/weights/best.pt --source /home/a/Desktop/Vision/KTJ/BEFORE/학위논문/data/768-marigold/yolo/test/images --dest /home/a/Desktop/Vision/AI-CHAMPION/DIA-YOLO-All-file/Test/result --conf 0.5 --alpha 0.5

def parse_args():

    parser = argparse.ArgumentParser(description="YOLO11-OBB 추론 및 투명 박스 그리기")

    parser.add_argument("--weights", type=str, required=True, help="모델 가중치 파일 경로")

    parser.add_argument("--source", type=str, required=True, help="추론할 이미지 폴더 경로 (폴더 A)")

    parser.add_argument("--dest", type=str, required=True, help="결과 저장 폴더 경로 (폴더 B)")

    parser.add_argument("--conf", type=float, default=0.25, help="신뢰도 임계값")

    parser.add_argument("--alpha", type=float, default=0.5, help="채워넣기 투명도 (0.0 ~ 1.0)")

    parser.add_argument("--device", type=str, default="0", help="연산 디바이스 (예: '0', 'cpu')")

    return parser.parse_args()



def get_rotated_rect_corners(xc, yc, w, h, angle_rad):

    # 사각형 네 모서리 (중심 기준)

    dx, dy = w / 2, h / 2

    corners = [(-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy)]

    pts = []

    cos_a = math.cos(angle_rad)

    sin_a = math.sin(angle_rad)

    for x0, y0 in corners:

        x = x0 * cos_a - y0 * sin_a + xc

        y = x0 * sin_a + y0 * cos_a + yc

        pts.append((int(x), int(y)))

    return pts



# 아래는 `def main():` 내부, for문부터 저장까지 수정된 코드입니다.
def main():
    args = parse_args()
    model = YOLO(args.weights)
    os.makedirs(args.dest, exist_ok=True)
    class_names = model.names
    np.random.seed(42)

    MAX_CLASSES = 15
    skipped_images = []  # (파일명, 사유) 저장

    # 클래스별 색상 고정 (BGR 포맷)
    colors = {
        0: (255, 0, 0),      # 파랑
        1: (0, 0, 255),      # 빨강
        2: (0, 255, 0),      # 초록
        3: (0, 128, 255),    # 주황
        4: (128, 0, 128),    # 보라
        5: (255, 255, 0),    # 청록
        6: (255, 0, 255),    # 분홍
        7: (0, 255, 255),    # 노랑
        8: (128, 128, 128),  # 회색
        9: (42, 42, 165),    # 갈색
        10: (102, 255, 102), # 연두
        11: (128, 0, 0),     # 진한 파랑
        12: (0, 0, 128),     # 진한 빨강
        13: (0, 128, 0),     # 진한 초록
        14: (0, 165, 255)    # 진한 노랑
    }

    for fname in os.listdir(args.source):
        src_path = os.path.join(args.source, fname)

        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
            skipped_images.append((fname, "unsupported extension"))
            continue
        if not os.path.isfile(src_path):
            skipped_images.append((fname, "not a file"))
            continue

        print(f"[DEBUG] Processing: {src_path}")
        img = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"[WARN] Failed to read: {src_path}")
            skipped_images.append((fname, "cv2 read failed"))
            continue

        if img.ndim != 3 or img.shape[2] != 4:
            print(f"[SKIP] Not a 4-channel image: {fname}")
            skipped_images.append((fname, "not 4-channel"))
            continue

        input_img = img.copy()             # 4채널 유지
        img_bgr = img[:, :, :3].copy()     # 시각화용 BGR 추출

        results = model.predict(source=src_path,
                                conf=args.conf,
                                device=args.device,
                                imgsz=768,
                                verbose=False)
        overlay = img_bgr.copy()

        for r in results:
            if r.obb is None or r.obb.data is None or r.obb.data.shape[0] == 0:
                print(f"[WARN] No OBB detections for {fname}")
                continue

            for xc, yc, w, h, angle, conf, cls in r.obb.data.tolist():
                cls = int(cls)
                if cls >= MAX_CLASSES:
                    continue
                print(f"[DEBUG] Detected class {cls} ({class_names[cls]}) with conf={conf:.3f}")
                corners = get_rotated_rect_corners(xc, yc, w, h, angle)
                pts = np.array(corners, np.int32).reshape((-1, 1, 2))
                color = colors[cls]
                cv2.fillPoly(overlay, [pts], color)
                cv2.polylines(overlay, [pts], True, color, 2)

        output = cv2.addWeighted(overlay, args.alpha, img_bgr, 1 - args.alpha, 0)
        dst_path = os.path.join(args.dest, fname)
        print(f"[DEBUG] Saving to: {dst_path}")
        cv2.imwrite(dst_path, output)
        print(f"Saved: {dst_path}")

    if skipped_images:
        print("\n🔍 Skipped images:")
        for name, reason in skipped_images:
            print(f" - {name} ({reason})")







if __name__ == "__main__":

    main()



