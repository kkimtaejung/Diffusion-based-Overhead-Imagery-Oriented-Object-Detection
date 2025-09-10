import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 입력 폴더 (모든 .npy 파일이 여기에 있음)
npy_folder = "./output/eval/PCB/5-1-256/PCB"
# 출력 폴더 (변환된 이미지 저장할 곳)
output_folder = "./output/eval/PCB/5-1-256/IMG"
os.makedirs(output_folder, exist_ok=True)

# 모든 .npy 파일 순회
for fname in os.listdir(npy_folder):
    if fname.endswith(".npy"):
        file_path = os.path.join(npy_folder, fname)
        arr = np.load(file_path)

        # 시각화를 위한 정규화 (0~255로 스케일링)
        norm = (arr - np.min(arr)) / (np.max(arr) - np.min(arr) + 1e-8)
        norm = (norm * 255).astype(np.uint8)

        # 단일 채널인 경우만 처리 (H, W) 또는 (1, H, W)
        if norm.ndim == 3 and norm.shape[0] == 1:
            norm = norm[0]

        # PIL로 저장
        out_img = Image.fromarray(norm)
        out_path = os.path.join(output_folder, fname.replace(".npy", ".png"))
        out_img.save(out_path)

print("✅ 저장 완료:", output_folder)
