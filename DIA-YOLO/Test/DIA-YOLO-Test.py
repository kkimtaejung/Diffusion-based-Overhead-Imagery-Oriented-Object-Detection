import sys
import os
import gc
import torch
import cv2
import numpy as np
import math
import argparse
CUSTOM_ULTRA_ROOT = "./Ultralytics Folder"
sys.path.insert(0, CUSTOM_ULTRA_ROOT)
for module in list(sys.modules.keys()):
    if module.startswith('ultralytics'):
        del sys.modules[module]
import ultralytics
print("✅ Using ultralytics from:", ultralytics.__file__)
from ultralytics import YOLO

# 사용법
# python DIA-YOLO-Test.py --weight ./runs/obb/PCB/weights/best.pt --source ./Data/YOLO/test/images --dest ./Result --conf 0.5 --alpha 0.5

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

def main():
    args = parse_args()
    model = YOLO(args.weights)
    os.makedirs(args.dest, exist_ok=True)
    class_names = model.names
    np.random.seed(42)

    MAX_CLASSES = 15
    skipped_images = []  # (파일명, 사유) 저장

    # 클래스별 색상 정의 (BGR 포맷)
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



