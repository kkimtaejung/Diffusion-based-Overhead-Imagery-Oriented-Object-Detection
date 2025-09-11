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
  <img src="figure/model-architecture.png" width="700" alt="f-AnoGAN architecture">
</div>

#### 세부 구조

<details>
 <summary> DFF(Diffusion-based Four-channel Fusion) 모듈  </summary>

- DFF 채널 융합 모듈에서는 디퓨전 기반의 Marigold 모델의 추론 기능만을 활용하여 2D 영상에서 1D 깊이 맵을 추정합니다.

- 이후 추정된 깊이 맵을 RGB 영상과 동일한 값의 범위(0 ~ 255)로 정규화를 진행합니다.

- 정규화된 깊이 맵 D와 RGB 영상과의 채널 축 합성을 진행하여 4채널의 RGBD 데이터를 취득합니다.
  
 <summary> Involution </summary>

- 기존 YOLO ver.11의 backbone에서 입력단의 Convolution을 Involution으로 대체합니다.

- Involution에서는 동적 커널을 통해 RGBD 데이터의 깊이 정보를 고려하여 위치별로 다른 커널 값을 적용하여 특징을 추출합니다.

 <summary> CBAM </summary>

- 기존 YOLO ver.11의 head에서 각 레이어 사이에 CBAM을 적용합니다.

- CBAM에서는 채널, 공간 주의(Channel, Spatial attention) 특징 맵을 통해 RGBD 데이터 속 깊이 정보를 풍부하게 활용합니다.

- 더불어 수직 촬영 영상의 특징인 초소형부터 대형 객체들이 밀집한 상태에서 어느 부분에 집중하여 검출을 진행할지 결정함으로써 검출 성능을 향상시킵니다.

</details>

<div align="center">
  <img src="figure/specific-architecture.png" width="700" alt="f-AnoGAN architecture">
</div>


-------------

## 데이터셋

<details>
 <summary> 카메라를 통해 표면과 수직이 되어 좌측과 같이 데이터 촬영, 객체 정보는 txt 형태로 취득하여 우측과 같이 시각화 </summary>

- 영상 데이터: PCB 자체 제작 데이터와 오픈소스 데이터를 활용하였습니다. 인공위성 오픈소스 데이터로는 DOTA 1.5, AITOD 데이터를 활용하였습니다.

- 객체 정보 데이터: 모든 데이터를 txt 형식으로 변환하여, <클래스 번호> <x1> <y1> ... <x4> <y4> 형태로 구성하였습니다.

</details>

<div align="center">
  <img src="figure/데이터구성.png" width="350" alt="f-AnoGAN architecture">
</div>

<details>
 <summary> 취득된 데이터의 모습 </summary>

- 상단 깊이 데이터는 Marigold 모델로부터 추정된 1채널의 깊이 맵입니다.

- 중단 RGBD 데이터는 채널 융합 모듈을 통해 생성된 4채널의 데이터입니다.

- 하단 라벨링 데이터는 txt 라벨 정보를 바탕으로 이미지에 바운딩박스 형태로 시각화한 모습입니다.

</details>

<div align="center">
  <img src="figure/데이터종류.png" width="700" alt="f-AnoGAN architecture">
</div>

--------------

## 코드 설명


<details>

Marigold (DFF 모듈)

  <summary> Marigold 학습 </summary>

  <summary> Marigold 추론 </summary>

</details>

<details>
  
DIA-YOLO

<summary> 모델 구성 </summary>
   
  * [모델 YAML 파일](Model/DIA-YOLO Model.yaml)
    * [모델 크기](https://github.com/kkimtaejung/Diffusion-based-Overhead-Imagery-Oriented-Object-Detection/blob/main/Model/DIA-YOLO Model.yaml#L0-L10)

  :
   

<summary> 학습 과정 </summary>

<summary> 테스트 과정 </summary>


</details>
 

 
  
  * [모델 전체 코드](models/MIN.py)
    * [제안하는 손실함수](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L33-L84)
    
    : 복원된 펼쳐진 위상 맵에 대한 균일함을 평가하는 Uniform loss, 높이 차이의 동일함을 평가하는 Height difference loss 설계
    * [모델 초기화](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L91-L218)
    
    : 첫 번째 스테이지 입력 위상 맵과 마스크, 두 번째 스테이지 입력 펼쳐진 위상 맵과 마스크 정의, 각 스테이지별 판별자, 생성자 정의, 파라미터 정의
    * [데이터 사전처리](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L220-L257)
    
    : 마스크 생성 과정을 기존과 달리 임의로 지정 (그림자와 빛 반사 영역에 대해)
    * [PAM(Position Adaptive Mask)](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L260-L329)
    
    : f-AnoGAN 학습된 모델로 이상치 영상 취득, 이상치 영상을 활용해 마스크 영상 생성
    * [모델 학습 과정](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L331-L393)
    
    : 학습 과정에서는 정답(그림자와 빛 반사가 없는)에 대해서만 학습을 진행
    * [모델 테스트 과정](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L403-L465)
    
    : 테스트 과정에서는 노이즈(그림자와 빛 반사가 존재하는)에 대해 테스트를 진행하며, 첫 스테이지 결과가 두 번째 스테이지로 이어짐
    * [모델 파라미터 갱신](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L468-L596)
    
    : 각각의 판별자, 생성자 갱신 과정에서 제안하는 손실함수 적용
    * [학습 출력 로그](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L598-L608), [학습/테스트 결과 시각화](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L610-L620), [학습된 모델 저장](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L622-L629), [테스트 모델 로드](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/models/MIN.py#L631-L634)

</details>

<details>

<summary> 모델 파라미터 설정 </summary> 

  * [모델 사전 설정 코드](train.py)
    
    * [데이터 경로 로드 설정](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L25-L27)
    
    : 모아레 영상과 마스크 영상이 담긴 폴더 경로 입력
    * [파라미터 설정](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L28-L79)
    
    : 모델 학습에 앞서 제약 조건을 정의
    * [학습 데이터 전처리 설정](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L81-L87)
    
    : 토치 변환, 정규화 등 실제 데이터 로드
    * [모델 로드 및 로그 설정](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L89-L100)
    
    : 모델 생성/로드/저장, 학습 수, 학습 시간, loss 로그 TXT 파일 생성

</details>

<details>

<summary> 학습 데이터 불러오기 </summary> 

  * [실제 데이터 로드 코드](util/data_load.py) 입니다.
  
    * [데이터 파일 로드](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/util/data_load.py#L20-L27)
    
    : 지정 형식에 따른 폴더 속 영상 및 마스크 파일 로드 및 정렬
    * [데이터 전처리](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/util/data_load.py#L29-L49)
    
    : 영상 및 마스크 크기 재설정, 토치 변환, 정규화 과정을 통해 학습에 맞게 재구성

</details>

<details>

<summary> 모델 학습 </summary> 

  * [모델 학습 코드](train.py)
    
    * [모델 저장](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L103-L110)
    
    : 모델 저장 주기, 경로 설정
    * [모델 학습 진행](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L113-L130)
    
    : 영상 및 마스크 전처리 후 모델에 입력 및 학습, loss 갱신
    * [학습 결과 저장](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/train.py#L133-L153)
    
    : 학습 후 결과 시각화하여 저장, 학습 수, 학습 시간 등 정보 출력

</details>

<details>

<summary> 테스트 데이터 불러오기 </summary> 

  * [테스트 데이터 로드 코드](util/data_load_test.py)
    * [데이터 파일 로드](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/util/data_load_test.py#L20-L26)
    
    : 앞선 학습과 달리 스테이지 마다 다른 영상이 입력되지 않고, 한 입력 영상으로 복원 진행
    * [데이터 전처리](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/util/data_load_test.py#L28-L41)
    
    : 학습 과정과 동일

</details>

<details>

<summary> 학습된 모델 테스트 </summary> 

  * [모델 테스트 코드](test.py)
    
    * [학습 모델 로드](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/test.py#L108-L110)
    
    : 학습된 모델 불러와 테스트에 활용
    * [테스트 데이터 전처리](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/test.py#L116-L122)
    
    : 학습 과정과 동일
    * [테스트 결과 시각화](https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction/blob/main/test.py#L125-L128)
    
    : 학습 과정과 동일, 결과 최종적으로 복원된 펼쳐진 위상 맵(Unwrap)으로 높이 복원 가능

</details

--------------

## 실행 가이드라인

* 레포지토리 클론
    ```
    git clone https://github.com/kkimtaejung/Research-for-Moire-3D-Reconstruction.git
    ```
* 가상환경에 라이브러리 설치
    ```
    pip install -r requirements.txt
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
@ARTICLE{10902408,
  author={Kim, Tae-Jung and Ha, Min-Ho and Arshad, Saba and Park, Tae-Hyoung},
  journal={IEEE Access}, 
  title={MIN: Moiré Inpainting Network With Position Adaptive Mask for 3-D Height Reconstruction}, 
  year={2025},
  volume={13},
  number={},
  pages={37501-37513},
  keywords={Image reconstruction;Printed circuits;Reflection;Generative adversarial networks;Context modeling;Height measurement;Integrated circuit modeling;Computational modeling;Solid modeling;Adaptive systems;Artificial intelligence;computer vision;generative adversarial networks;image inpainting;anomaly detection;Moiré;printed circuit board},
  doi={10.1109/ACCESS.2025.3545748}}
```

--------------
## Acknowledgments
This project is based on [CSA-inpainting](https://github.com/KumapowerLIU/CSA-inpainting), and we have modified the model structure for our specific research objectives.
