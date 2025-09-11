import sys
sys.path.insert(0, './Ultralytics Folder')
if 'ultralytics' in sys.modules:
    del sys.modules['ultralytics']
import ultralytics
print(f"현재 Ultralytics 폴더 경로: {ultralytics.__file__}")
from ultralytics import YOLO

# 모델 파일 경로 (채널 수: 4)
model_yaml_path = "./Model/DIA-YOLO Model.yaml"

# 모델 생성
model = YOLO(model_yaml_path)

# 모델 정보 출력
model.info()

# 학습 시작
results = model.train(	
    data="./Data/YOLO/data.yaml",  # 데이터 폴더 속 yaml 파일 경로
    epochs=1000000,                 # 학습 횟수
    imgsz=1024,                     # 이미지 크기
    batch=1,                        # 배치 사이즈
    patience=50,                    # 50번의 성능 향상이 없다면 종료
    name='PCB',                     # 결과 저장될 폴더 이름
    iou=0.9,                        # IoU 향상을 위함
    #pretrained=False,              # 본 논문에서 수직 촬영 영상은 보편적인 도메인과 특징이 달라 사전학습 가중치를 활용하지 않는 것이 성능이 좋았음
    device=[1],                     # 멀티 GPU 사용 시 [0,1...]
    save=True,
    save_period=-1,                 # 매 epoch 마다 저장되어 용량 차는 걸 방지, 최고 모델과 마지막 모델만 저장
)


