# audi_minutes
- 영상들 중에서 거의 유사한 오디오끼리 묶는 프로그램

## 요청사항
- 영상 파일들 중에서 오디오가 유사한 영상끼리 짝지어서 각 각 폴더 안에 넣음

## 프로젝트 설계
1. 영상에서 오디오 추출
2. 오디오에서 특성 추출
3. 유사도 계산(코사인 유사도 계산)
4. 같은 오디오를 가진 영상 골라내기
5. 골라진 영상들끼리 같은 폴더 안에 넣기
6. 배포하기 위해 ffmpegInstaller 생성(필수 설치)
7. audi_minutes.exe 실행파일 생성

## 프로그램 사용방법
- `audi_minutes.exe`와 같은 경로에 `videos` 폴더가 있어야 한다. (폴더 안에 영상 파일들이 들어가 있으면 된다.)
- `*.mp4` 파일이어야 한다.
- `ffmpegInstaller` 설치해야 한다.
- `audi_minutes.exe` 실행하면 된다.

## 프로그램 다운로드
- [ffmpegInstaller](https://drive.google.com/file/d/1iUPL9IkJgkhaJiuBPyb9EuFkELSMjkbW/view?usp=drive_link)
- [audi_minutes.exe](https://drive.google.com/file/d/1acD-vNzYKNf8Hg4ceP5QfW6cps4vT8id/view?usp=drive_link)



## 결과
- 영상 6개의 파일로 실험 결과 거의 유사한 오디오끼리 잘 묶였다.
- 파라미터를 아래와 같이 0.17로 줬더니 성공했다.
```
threshold = 0.17
```
