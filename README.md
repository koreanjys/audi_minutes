# audi_minutes
- 영상들 중에서 거의 유사한 오디오끼리 묶는 프로그램

## 요청사항
- 영상 파일들 중에서 오디오가 유사한 영상들을 그룹화 시켜서 각 폴더에 넣음

## 프로젝트 설계
1. 영상에서 오디오 추출
2. 오디오에서 특성 추출
3. 유사도 계산(코사인 유사도 계산)
4. 같은 오디오를 가진 영상 골라내기
5. 골라진 영상들끼리 같은 폴더 안에 넣기
6. 배포하기 위해 ffmpegInstaller 생성(필수 설치)
7. audi_minutes.exe 실행파일 생성

## 프로그램 진행도

1. 동영상 파일로부터 오디오 추출: `extract_audio_from_video` 함수는 동영상 파일로부터 오디오를 추출하여 임시 WAV 오디오 파일을 생성합니다.

2. 오디오 특징 추출: `extract_features` 함수는 librosa 라이브러리를 사용하여 주어진 오디오 파일에서 MFCC (Mel-frequency cepstral coefficients) 기반의 특징을 추출합니다.

3. 오디오 유사성 계산: `compute_similarity_by_segments` 함수는 입력된 두 오디오 특징 사이의 코사인리를 계산하여 그 오디오들이 얼마나 유사한지를 결정합니다.

4. 비슷한 오디오의 동영상 그룹화 `group_similar_videos` 함수는 유사한 오디오를 가진 동영상 파일을 그룹화하는 데 사용되며, 각 동영상은 하나 이상의 그룹에 속할 수 있습니다.룹화는 `is_video_similar` 함수를 사용하여 이미 그룹화된 오디오와 비교하여진행됩니다.

5. 가장 외부의 `main` 함수: 모든 동영상으로부터 오디오 파일을 추출하고, 오디오 특징을 추출한 다음, 그룹화된 비슷한 오디오영상을 출력합니다.

6. 그룹화된 동영상 파일 이동: `move_videos_to_folders` 함수는 생성된 그룹별로 개별 폴더에영상 파일들을 복사하여 그룹화 결과를 계층적으로 저장합니다.

## 프로그램 사용방법
- `audi_minutes.exe`와 같은 경로에 `videos` 폴더가 있어야 한다. (폴더 안에 영상 파일들이 들어가 있으면 된다.)
- `*.mp4` 파일이어야 한다.
- `ffmpegInstaller` 설치해야 한다.
- `audi_minutes.exe` 실행하면 된다.

## 프로그램 다운로드
- [ffmpegInstaller](https://drive.google.com/file/d/1iUPL9IkJgkhaJiuBPyb9EuFkELSMjkbW/view?usp=drive_link)
- [audi_minutes.exe](https://drive.google.com/file/d/1sYqeRo6jBLoEif2Ub_55J5pOdU-nEr5n/view?usp=drive_link)



## 결과
- 영상 6개의 파일로 실험 결과 거의 유사한 오디오끼리 잘 묶였다.
- 파라미터를 아래와 같이 0.17로 줬더니 성공했다.
```
threshold = 0.17
```
