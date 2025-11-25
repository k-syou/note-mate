# 🚀 Quick Start Guide - Backend Server

AI 악보 처리 서비스 백엔드를 빠르게 시작하는 가이드입니다.

## ⚡ 빠른 시작 (3단계)

### 1️⃣ 가상환경 생성 및 활성화

```bash
cd Server
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2️⃣ 의존성 설치

```bash
pip install -r requirements.txt
```

> ⏱️ 설치 시간: 약 2-3분 소요

### 3️⃣ 서버 실행

```bash
python app.py
```

서버가 `http://localhost:5000`에서 실행됩니다! 🎉

---

## ✅ 설치 확인

설치가 제대로 되었는지 확인하려면:

```bash
python test_setup.py
```

모든 테스트가 통과하면 준비 완료입니다!

---

## 🧪 API 테스트

### 헬스 체크
```bash
curl http://localhost:5000/
```

### 파일 업로드 테스트
```bash
curl -X POST -F "file=@path/to/your/sheet-music.png" http://localhost:5000/api/upload
```

---

## 📁 프로젝트 구조

```
Server/
├── 📄 app.py                 # Flask 메인 애플리케이션
├── ⚙️ config.py              # 설정 파일
├── 🔧 utils.py               # 유틸리티 함수
├── 🎼 omr_processor.py       # OMR 처리 모듈
├── 🎵 music_processor.py     # 음악 처리 모듈
├── 📋 requirements.txt       # Python 의존성
├── 📖 README.md              # 상세 문서
├── 🧪 test_setup.py          # 설치 확인 스크립트
├── 📂 uploads/               # 업로드된 이미지
├── 📂 outputs/               # 처리된 파일
├── 📂 temp/                  # 임시 파일
└── 📂 models/                # AI 모델 (향후 사용)
```

---

## 🎯 주요 기능

✨ **악보 이미지 업로드** - PNG, JPG, PDF 지원  
🔍 **OMR (악보 인식)** - oemer 라이브러리 사용  
🎹 **MIDI 변환** - 인식된 악보를 MIDI로 변환  
⚡ **난이도 조정** - Easy, Medium, Original 3단계  
📥 **파일 다운로드** - MusicXML, MIDI 형식 지원

---

## 🔧 문제 해결

### ❌ oemer 설치 오류
```bash
# MuseScore 설치 필요
# Windows: https://musescore.org/download
# Ubuntu: sudo apt-get install musescore
```

### ❌ music21 설정 오류
```python
from music21 import configure
configure.run()
```

### ❌ 포트 충돌
`.env` 파일을 생성하고 다른 포트 지정:
```
PORT=8000
```

---

## 📚 더 알아보기

- 📖 [전체 API 문서](README.md)
- 📋 [구현 계획서](../Documents/ImplementationPlan.md)
- 🎵 [프로젝트 개요](../README.md)

---

## 💡 다음 단계

1. ✅ 백엔드 서버 실행 완료
2. 🎨 프론트엔드 개발 시작
3. 🔗 백엔드-프론트엔드 통합
4. 🧪 전체 시스템 테스트

---

**문제가 있나요?** 
- `test_setup.py`를 실행하여 설치 상태 확인
- `README.md`에서 상세 문서 확인
- GitHub Issues에 문제 보고

**준비 완료!** 🚀
