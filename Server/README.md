# AI Music Score Service - Server

Flask 기반 백엔드 서버로 악보 이미지 인식(OMR), 음악 처리, MIDI 변환 기능을 제공합니다.

## 📁 프로젝트 구조

```
Server/
├── app.py                 # Flask 메인 애플리케이션
├── config.py             # 설정 파일
├── utils.py              # 유틸리티 함수
├── omr_processor.py      # OMR 처리 모듈
├── music_processor.py    # 음악 처리 모듈
├── requirements.txt      # Python 의존성
├── uploads/              # 업로드된 이미지 저장
├── outputs/              # 처리된 파일 저장
└── temp/                 # 임시 파일
```

## 🚀 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
python app.py
```

서버는 기본적으로 `http://localhost:5000`에서 실행됩니다.

## 📡 API 엔드포인트

### 1. 파일 업로드
```http
POST /api/upload
Content-Type: multipart/form-data

파라미터:
- file: 악보 이미지 파일 (PNG, JPG, JPEG, PDF)

응답:
{
  "success": true,
  "message": "File uploaded successfully",
  "data": {
    "file_id": "unique-file-id",
    "filename": "original-filename.png"
  }
}
```

### 2. 악보 인식 (OMR)
```http
POST /api/recognize
Content-Type: application/json

바디:
{
  "file_id": "unique-file-id",
  "preprocess": true
}

응답:
{
  "success": true,
  "message": "Sheet music recognized successfully",
  "data": {
    "file_id": "unique-file-id",
    "musicxml_path": "/path/to/output.musicxml",
    "metadata": {
      "title": "악보 제목",
      "num_notes": 150,
      "num_measures": 32,
      ...
    }
  }
}
```

### 3. 난이도 조정
```http
POST /api/simplify
Content-Type: application/json

바디:
{
  "file_id": "unique-file-id",
  "level": "easy"  // "easy", "medium", "original"
}

응답:
{
  "success": true,
  "message": "Score simplified to easy level",
  "data": {
    "file_id": "unique-file-id",
    "level": "easy",
    "musicxml_path": "/path/to/simplified.musicxml",
    "midi_path": "/path/to/simplified.mid",
    "score_info": { ... }
  }
}
```

### 4. MIDI 변환
```http
POST /api/convert
Content-Type: application/json

바디:
{
  "file_id": "unique-file-id"
}

응답:
{
  "success": true,
  "message": "Converted to MIDI successfully",
  "data": {
    "file_id": "unique-file-id",
    "midi_path": "/path/to/output.mid"
  }
}
```

### 5. 파일 다운로드
```http
GET /api/download/<file_id>/<file_type>

file_type:
- musicxml: 원본 MusicXML
- midi: 원본 MIDI
- simplified_easy: 쉬운 버전 MIDI
- simplified_medium: 중간 버전 MIDI
```

### 6. 처리 상태 확인
```http
GET /api/status/<file_id>

응답:
{
  "success": true,
  "data": {
    "file_id": "unique-file-id",
    "status": "recognized",
    "metadata": { ... }
  }
}
```

## ⚙️ 설정

`config.py`에서 다음 설정을 변경할 수 있습니다:

- `MAX_FILE_SIZE`: 최대 파일 크기 (기본: 10MB)
- `ALLOWED_EXTENSIONS`: 허용된 파일 확장자
- `DEFAULT_TEMPO`: 기본 템포 (기본: 120 BPM)
- `SIMPLIFICATION_LEVELS`: 난이도별 설정

## 🎵 난이도 조정 기능

### Easy (쉬운 버전)
- 템포: 70% 속도
- 리듬 단순화: 활성화
- 화음 단순화: 활성화
- 장식음 제거: 활성화

### Medium (중간 버전)
- 템포: 85% 속도
- 리듬 단순화: 활성화
- 화음 단순화: 비활성화
- 장식음 제거: 활성화

### Original (원본)
- 템포: 100% 속도
- 모든 단순화 비활성화

## 🔧 기술 스택

- **Flask**: 웹 프레임워크
- **oemer**: OMR 엔진
- **music21**: 음악 처리 및 분석
- **OpenCV**: 이미지 전처리
- **Pillow**: 이미지 처리

## 📝 개발 노트

### OMR 처리 과정
1. 이미지 전처리 (그레이스케일, 이진화, 노이즈 제거)
2. oemer 라이브러리로 악보 인식
3. MusicXML 형식으로 변환
4. music21로 검증 및 메타데이터 추출

### 음악 처리 과정
1. MusicXML 파싱
2. 난이도별 변환 적용
3. MIDI 파일 생성
4. 결과 파일 저장

## 🐛 문제 해결

### oemer 설치 오류
```bash
# MuseScore 설치 필요 (MusicXML 렌더링용)
# Windows: https://musescore.org/download
# Linux: sudo apt-get install musescore
```

### music21 설정
```python
# 처음 실행 시 환경 설정 필요
from music21 import configure
configure.run()
```

## 📄 라이선스

MIT License
