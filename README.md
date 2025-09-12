# DIA-YOLO: Diffusion-Based Involution Attention YOLO for Overhead Imagery
[IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11142761) |[IEEE ACCES 2025 paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11142761)| [BibTex](#jump1)

-----------
## 요약
<!-- 2. 그림자/둥근 모서리 CSS 적용 -->
<div align="center">
  <img src="figure/dia-yolo-architecture.png"
       alt="모아레 패턴 예시"
       style="width:1240px; max-width:90%; border-radius:28px; box-shadow:0 20px 18px #0002; margin-bottom: 16px;">
</div>

<details>
 <summary> 2D 수직 촬영 영상의 고속·정밀 객체 검출을 위해 특화된 생성형 기반의 모델 설계 </summary>

- 수직 촬영 영상(Overhead Imagery)이란 촬영되는 카메라와 표면 위의 객체가 직각이 되도록하여 촬영된 영상입니다. 수직 촬영 영상의 예시로는 인쇄회로기판(PCB, Printed Circuit Board), 인공위성, 드론, 세포 등의 영상들이 존재합니다. 

- 수직 촬영 영상 중 인공위성, PCB의 공통적인 특징은 초소형(수십 픽셀)의 객체부터 대형 객체까지 혼재하고, 한 영상 속 객체들이 다수 밀집하게 분포하여 있습니다. 이러한 특징은 객체 검출을 어렵게 합니다.

- 따라서 기존의 수직 촬영 영상의 특징을 강화하는 디퓨전 기반 채널 융합 모듈을 제안하고, 강화된 RGBD 4채널 데이터를 입력으로 재구성된 DIA-YOLO(Diffusion-based Involution Attention YOLO)모델을 통해 검출의 성능과 속도를 획기적으로 향상시킵니다.

- 최종적으로 2D 수직 촬영 영상에 대한 정밀한 실시간 객체 검출을 진행하여 PCB 불량 검사, 재난 모니터링 등의 어플리케이션에 활용할 수 있습니다.

</details>

-------------

## 제안 방식

#### 모델 구조

<details>
 <summary> 채널 융합 모듈과 모델로 이어지는 구조로 영상의 특징을 강화하고 이를 고려하여 설계된 네트워크를 통한 고속·정밀 객체 검출까지의 과정 </summary>

- 채널 융합 모듈에서는 디퓨전 기반 Marigold 모델을 통해 추정한 깊이 맵을 활용합니다. 깊이 맵 D와 RGB 영상 간의 채널 축 융합을 통해 4채널의 RGBD 데이터를 생성합니다.

- 네트워크에서는 Involution, CBAM(Convolution Block Attention Module)을 적용하여 깊이 정보를 고려한 수직 촬영 영상에 특화된 객체 검출을 진행합니다.

- 최종적으로 검출된 결과를 영상에 바운딩 박스 형태로 시각화여 다양한 실시간 어플리케이션에 활용합니다.

</details>

<div align="center">
  <img src="figure/model-architecture.png" width="1000" alt="f-AnoGAN architecture">
</div>

#### 세부 구조

<details>
 <summary> DFF(Diffusion-based Four-channel Fusion) 모듈  </summary>

- DFF 채널 융합 모듈에서는 디퓨전 기반의 Marigold 모델의 추론 기능만을 활용하여 2D 영상에서 1D 깊이 맵을 추정합니다.

- 이후 추정된 깊이 맵을 RGB 영상과 동일한 값의 범위(0 ~ 255)로 정규화를 진행합니다.

- 정규화된 깊이 맵 D와 RGB 영상과의 채널 축 합성을 진행하여 4채널의 RGBD 데이터를 취득합니다.

</details>

<details>

 <summary> Involution </summary>

- 기존 YOLO ver.11의 backbone에서 입력단의 Convolution을 Involution으로 대체합니다.

- Involution에서는 동적 커널을 통해 RGBD 데이터의 깊이 정보를 고려하여 위치별로 다른 커널 값을 적용하여 특징을 추출합니다.

</details>

<details>

 <summary> CBAM </summary>

- 기존 YOLO ver.11의 head에서 각 레이어 사이에 CBAM을 적용합니다.

- CBAM에서는 채널, 공간 주의(Channel, Spatial attention) 특징 맵을 통해 RGBD 데이터 속 깊이 정보를 풍부하게 활용합니다.

- 더불어 수직 촬영 영상의 특징인 초소형부터 대형 객체들이 밀집한 상태에서 어느 부분에 집중하여 검출을 진행할지 결정함으로써 검출 성능을 향상시킵니다.

</details>

<div align="center">
  <img src="figure/specific-architecture.png" width="800" alt="f-AnoGAN architecture">
</div>


-------------

## 데이터셋

<details>
 <summary> 카메라를 통해 표면과 수직이 되어 좌측과 같이 데이터 촬영, 객체 정보는 txt 형태로 취득하여 우측과 같이 시각화 </summary>

- 영상 데이터: PCB 자체 제작 데이터와 오픈소스 데이터를 활용하였습니다. 인공위성 오픈소스 데이터로는 DOTA 1.5, AITOD 데이터를 활용하였습니다.

- 객체 정보 데이터: 모든 데이터를 txt 형식으로 변환하여, <클래스 번호> <x1> <y1> ... <x4> <y4> 형태로 구성하였습니다.

</details>

<div align="center">
  <img src="figure/데이터구성.png" width="1000" alt="f-AnoGAN architecture">
</div>

<details>
 <summary> 취득된 데이터의 모습 </summary>

- 상단 깊이 데이터는 Marigold 모델로부터 추정된 1채널의 깊이 맵입니다.

- 중단 RGBD 데이터는 채널 융합 모듈을 통해 생성된 4채널의 데이터입니다.

- 하단 라벨링 데이터는 txt 라벨 정보를 바탕으로 이미지에 바운딩박스 형태로 시각화한 모습입니다.

</details>

<div align="center">
  <img src="figure/데이터종류.png" width="800" alt="f-AnoGAN architecture">
</div>

--------------

## 코드 설명


<details>
 <summary> Marigold (DFF 모듈) </summary>

  * [학습 코드](Marigold/train.py)

    * [경로 설정](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/Marigold/train.py#L34-L38)

      ⮑ 학습 진행 시 원래는 데이터셋 경로 및 체크포인트 경로를 설정해주어야 함, 해당 코드에서 미리 경로만 설정해두면 이후 사용시 문제없음
      ⮑ 데이터셋은 Hypersim에 예시로 만들어 둔 형태를 활용, train 폴더를 tar로 압축하여 Hypersim 에 놓고 사용

    * [데이터 파일 이름 설정](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/Marigold/data_split/hypersim)

      ⮑ TXT 파일

  * [추론 코드](Marigold/infer.py)

    

</details>

<details>
 <summary> DIA-YOLO </summary>
  
  * [모델 구성 파일](DIA-YOLO/Model/DIA-YOLO-Model.yaml)
    
    * [모델 설정](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Model/DIA-YOLO-Model.yaml#L1-L9)

      ⮑ 클래스 개수, 입력 채널 수, 모델 크기(n, s, m, l, x) 설정

    * [Backbone](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Model/DIA-YOLO-Model.yaml#L11-L23)
   
      ⮑ 기존의 YOLO 11 OBB와 다른 점은 입력단이 Involution으로 대체되었음

      * [Involution](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Ultralytics-Folder/ultralytics/nn/modules/conv.py/#L27-L49)
     
        ⮑ 4채널이 입력되도록 하기위해 직접 Ultralytics 폴더에 접근하여 Involution 함수를 정의하고 4채널에 맞게 설계해줌 (* yaml 파일만 번경하면 안됨 주의.)

    * [Head](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Model/DIA-YOLO-Model.yaml#L25-L46)
   
      ⮑ 기존의 YOLO 11 OBB와 다른 점은 Concat 이후 사이사이에 CBAM(Convolution Block Attention Module)이 추가됨

      * [CBAM](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Ultralytics-Folder/ultralytics/nn/modules/conv.py/#L51-L87)
     
        ⮑ Ultralytics 에 내부적으로 제공, 직접 구현해둠
  
  * [학습 코드](DIA-YOLO/Train/DIA-YOLO-Train.py)

    * [Ultralytics 경로 설정](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Train/DIA-YOLO-Train.py#L1-L7)
   
      ⮑ Ultralytics 는 YOLO 학습 시 자동으로 생성되지만, 사용자가 직접 정의하여 내부 파일을 수정함으로써 커스텀 모델 학습이 가능

    * [모델 정의](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Train/DIA-YOLO-Train.py#L9-L16)
   
      ⮑ 앞선 모델 구성 파일 YAML 경로를 불러와 모델을 생성하고, info()를 통해 4채널 입력 설정이 되었는지 확인

    * [학습](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Train/DIA-YOLO-Train.py#L18-L31)
   
      ⮑ YOLO에서는 다양한 학습 파라미터를 제공, 핵심은 데이터가 저장된 폴더 속 data.yaml 파일을 만들어야 함

      * [데이터 구성 파일](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Data/YOLO/data.yaml/#L1-L7)
     
        ⮑ YOLO 데이터는 train/valid/test 폴더 속 이미지(images)/라벨(labels) 폴더로 구성되며 txt 형식을 이룸, 클래스 개수와 각 클래스별 번호 및 이름 정의

  * [테스트 코드](DIA-YOLO/Test/DIA-YOLO-Test.py)

    * [Ultralytics 경로 설정](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Test/DIA-YOLO-Test.py#L1-L16)

    * [사용법](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Test/DIA-YOLO-Test.py#L18-L29)

      ⮑ 파이썬 파일을 실행할 때 조건 및 경로를 지정

    * [기울어진 객체 처리](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Test/DIA-YOLO-Test.py#L31-L41)

      ⮑ 지향적 객체 검출(Oriented Object Bounding Box) 모델에서는 출력된 결과에서 기울기를 계산

    * [클래스별 검출 색상 지정](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Test/DIA-YOLO-Test.py#L50-L70)

      ⮑ 모델은 검출 결과를 수치로 전달하기 때문에 이를 시각화하는 과정에서 직접 클래스에 따른 색상을 지정해야 함

    * [모델 검출](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Test/DIA-YOLO-Test.py#L91-L98)

      ⮑ 입력이 4채널이기 때문에 시각화하여 저장하기 위한 3채널 BGR 이미지를 따로 정의, results에는 모델의 검출 결과가 저장되며 저장경로, confidence, 이미지 크기 등에 대한 조건이 반영

    * [결과 처리](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/DIA-YOLO/Test/DIA-YOLO-Test.py#L100-L119)

      ⮑ results 속 OBB 결과에서 좌표 및 기울기 정보를 추출하여 시각화용 이미지에 라벨링하여 이미지로 저장
   
    
</details>

--------------

## Marigold 실행 가이드라인

* 레포지토리 클론
    ```
    git clone https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction.git
    ```
* 가상환경에 라이브러리 설치
    ```
    pip install -r Marigold/requirements.txt
    pip install -r Marigold/requirements+.txt
    pip install -r Marigold/requirements++.txt
    ```
* 학습 사전 설정
  * 기존 깃허브 [Marigold](https://github.com/prs-eth/Marigold)에서는 여러 데이터셋에 대해 학습을 진행하지만, 커스텀 데이터 학습을 위해 Hypersim 만 학습되도록 재구성함
  * train.py 경로 설정: 기본적으로 정의된 Hypersim 폴더 이름은 수정하지 않음(해당 이름으로 데이터셋을 불러오기에 내부 데이터만 바꿔주면 됨)
    ```
    os.environ['BASE_DATA_DIR'] = './Hypersim'
    os.environ['BASE_CKPT_DIR'] = './checkpoint'
    base_data_dir = os.environ['BASE_DATA_DIR']
    base_ckpt_dir = os.environ['BASE_CKPT_DIR']
    ```
  * 데이터 파일 이름 설정: Hypersim 폴더 참고하여 데이터셋을 구성, [데이터 파일 이름](Marigold/data_split/hypersim)에서 아래와 같은 구성으로 데이터 파일 이름 변경

    폴더, 파일 이름은 수정하지 않고 이미지를 바꿔넣는 방식을 추천(사유는 학습에서 파일 이름으로 불러오기 때문)

    앞은 rgb 이미지, 뒤는 depth 이미지

    ```
    ./ai_001_002/rgb_cam_00_fr0000.png ./ai_001_002/depth_plane_cam_00_fr0000.png
    ./ai_001_002/rgb_cam_00_fr0001.png ./ai_001_002/depth_plane_cam_00_fr0001.png
    ./ai_001_002/rgb_cam_00_fr0002.png ./ai_001_002/depth_plane_cam_00_fr0002.png
    ./ai_001_002/rgb_cam_00_fr0003.png ./ai_001_002/depth_plane_cam_00_fr0003.png
    ./ai_001_002/rgb_cam_00_fr0004.png ./ai_001_002/depth_plane_cam_00_fr0004.png
    ```
  * Tar 파일 설정: 학습 시 Tar 파일에서 데이터를 불러오기 때문에 Hypersim 폴더 내부 train 폴더를 tar로 압축 생성
    * 이때 valid tar 파일도 설정해야 하며, 위에서 txt 파일에 정의한 이름으로 불러오기 때문에 같은 경로로 설정해줌
    ```
    tar -cf hypersim/hypersim_processed_train.tar -C Hypersim/hypersim train
    tar -cf hypersim/hypersim_processed_val.tar -C Hypersim/hypersim train
    ```
* 학습 시작
  * 이때 실행되면 한 번 락이 걸리기 때문에 Ctrl + C 눌러줘야 함
    ```
    python train.py
    ```
* 테스트 사전 설정
  * .yaml 경로 설정: 추론에 앞서 추론할 데이터 경로를 직접 지정하여 설정할 수 있음
    ```
    name: hypersim                # 건들이면 피곤해짐
    disp_name: hypersim_val_all   # 이것도 건들일 필요없이 그냥 사용
    dir: ./Inference-Datasets/PCB-Mirtec/PCB.tar                # 학습과 동일한 형태의 tar 데이터 파일
    filenames:./Inference-Datasets/PCB-Mirtec/pcb-mirtec.txt    # 데이터 파일 이름 위 학습과 동일한 형태로 설정
    ```
  * .sh 경로 설정: 추론에서는 sh 파일을 실행시키기 때문에 [.sh 파일 경로](Marigold/script/eval)에서 sh 파일을 수정해야 함
    ```
    #!/usr/bin/env bash
    set -e
    set -x

    export BASE_DATA_DIR='./Inference-Datasets/PCB-Mirtec' # 추론 데이터 폴더 경로(폴더 이름 임의 지정 가능)

    # Use specified checkpoint path, otherwise, default value
    ckpt=${1:-"prs-eth/marigold-v1-0"} # 여기서는 기존 깃허브에 사전학습된 모델을 추론용도로만 사용
    subfolder=${2:-"eval"}

    python infer.py  \
        --checkpoint $ckpt \
        --seed 1234 \
        --base_data_dir $BASE_DATA_DIR \
        --denoise_steps 5 \               # step 수가 올라갈수록 품질 향상, 추론 시간 늘어남
        --ensemble_size 1 \               # size 수가 올라갈수록 품질 향상, 추론 시간 늘어남
        --dataset_config config/dataset/PCB.yaml \          # 앞선 yaml 파일 경로
        --output_dir output/${subfolder}/PCB/5-1-256 \      # 결과 저장할 폴더 이름
        --processing_res 256 \                              # 추론 결과 이미지 사이즈
        --resample_method bilinear \
        --output_processing_res \
    ```
* 테스트 시작
  * 256, 1024 사이즈별로 sh 파일 실행, 커스텀 가능
  * 이때 추론 결과는 npy 형식으로 [추론 결과 경로](Marigold/output/eval)에 지정했던 폴더 이름으로 존재
    ```
    bash script/eval/256-PCB-inference.sh
    bash script/eval/1024-PCB-inference.sh
    ```
* 시각화 후 RGBD 데이터 생성
  * [이미지로의 시각화](Marigold/output/npy-image.py)에서 입력, 출력 폴더 경로 수정 후 아래로 실행
    ```
    python npy-image.py
    ```
  * 이후 시각화 과정은 코드없이 핵심만 아래에 설명
    * npy 파일은 깊이 맵으로 값의 범위가 1000 이상으로 구성되며, 이를 0~255값으로 정규화해야 함
    * RGB와 정규화된 NPY를 채널 축으로 Concat 하여 4채널 데이터 구성

## DIA-YOLO 실행 가이드라인

* 레포지토리 클론
    ```
    git clone https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction.git
    ```
* 가상환경에 라이브러리 설치
  * Marigold 모델로 추론
    ```
    pip install -r DIA-YOLO/requirements.txt
    ```
* train.py 에 데이터셋 경로 할당
    ```
    self.dataroot= r'첫 번째 스테이지(First stage)의 정답 2D PCB 위상 맵(Phase map) 폴더 경로'
    self.maskroot= r'그림자와 빛 반사 영역에 대한 마스크 영상 폴더 경로'
    self.unwraproot = r'두 번재 스테이지(Second stage)의 정답 2D PCB 펼쳐진 위상 맵(Unwrap) 폴더 경로'
    ```
* 학습된 [f-AnoGAN](https://github.com/tSchlegl/f-AnoGAN) 모델 파일을 아래의 위치에 저장 (사전 학습된 모델 파일 [PCB1, PCB2, PCB3](https://drive.google.com/drive/folders/1qUL9Ps7Nco9pV27ChnksvblpD24lYnpv?usp=sharing))
    ```
    models/results/PCB1/discriminator
    models/results/PCB1/encoder
    models/results/PCB1/generator
    ```
* 학습 시작
    ```
    python train.py
    ```
* 테스트 시작
    ```
    python test.py
    ```


--------------

## <span id="jump1">Citation</span>
```
@ARTICLE{11142761,
  author={Kim, Tae-Jung and Park, Tae-Hyoung},
  journal={IEEE Access}, 
  title={DIA-YOLO: Diffusion-Based Involution Attention YOLO for Overhead Imagery}, 
  year={2025},
  volume={13},
  number={},
  pages={150570-150582},
  keywords={Feature extraction;YOLO;Real-time systems;Printed circuits;Diffusion models;Kernel;Indexes;Data models;Computational modeling;Training;Oriented object detection;overhead imagery;diffusion model;YOLO;involution;convolutional block attention module},
  doi={10.1109/ACCESS.2025.3603214}}
```

--------------
## Acknowledgments
This project is based on [YOLO 11 OBB](https://github.com/ultralytics/ultralytics), and we have modified the model structure for our specific research objectives.
This project also based on [Marigold](https://github.com/prs-eth/Marigold), and we have used the model inference for our specific research objectives.
