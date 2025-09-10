import sys
sys.path.insert(0, './Ultralytics Folder')

# 만약 ultralytics가 이미 import된 경우 제거
if 'ultralytics' in sys.modules:
    del sys.modules['ultralytics']

import ultralytics
print(f"✅ Using ultralytics from: {ultralytics.__file__}")
from ultralytics import YOLO

# YAML 정의된 모델 (ch: 4 포함됨)
model_yaml_path = "./Model/DIA-YOLO Model.yaml"

# YOLO 모델 생성
model = YOLO(model_yaml_path)

# 모델 정보 출력
model.info()

# 학습 수행
results = model.train(	
    data="./Data/YOLO/data.yaml",  # your data.yaml
    epochs=1000000,
    imgsz=1024,
    batch=1,
    patience=50,
    name='PCB',
    iou=0.9,
    #pretrained=False,
    device=[1],             # ✅ 멀티 GPU 사용
    save=True,
    save_period=-1,            # ✅ 매 epoch 저장 X
)


