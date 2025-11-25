# 🎵 AI 악보 처리 서비스 구현 계획

악보 이미지를 입력받아 자동으로 연주하거나 쉬운 버전으로 변환해주는 AI 기반 웹 서비스를 구축합니다. **피아노와 기타 악보**를 우선 지원하며, 향후 **타브악보**까지 확장할 예정입니다.

---

## 📋 개발 로드맵

### Phase 1: MVP (사전 학습 모델 활용) ⭐ 현재 구현 목표
- `oemer` 라이브러리를 사용한 OMR 구현
- 피아노, 기타 표준 악보 인식
- 기본 재생 및 난이도 조정 기능
- 웹 인터페이스 구축

### Phase 2: 성능 개선 (커스텀 모델 학습)
- 실사용 데이터 수집 및 분석
- 피아노/기타 특화 모델 파인튜닝
- 인식 정확도 향상
- 모델 학습 파이프라인 구축

### Phase 3: 기능 확장
- 타브악보(Guitar Tab) 인식 추가
- 다양한 난이도 조정 옵션
- 악보 편집 기능
- 멀티트랙 지원

---

## 🔍 User Review Required

> [!IMPORTANT]
> **Phase 1 기술 스택 (MVP)**
> - **OMR 엔진**: `oemer` (사전 학습 모델, 즉시 사용 가능)
> - **음악 처리**: `music21` (악보 분석, 조작, MusicXML/MIDI 변환)
> - **백엔드**: Python Flask 또는 FastAPI
> - **프론트엔드**: HTML/CSS/JavaScript (모던 UI)
> - **음악 재생**: Tone.js (웹 기반 음악 재생)
> - **악보 렌더링**: VexFlow 또는 OpenSheetMusicDisplay

> [!NOTE]
> **Phase 2 이후 추가 예정**
> - 커스텀 OMR 모델 학습 파이프라인 (PyTorch/TensorFlow)
> - 타브악보 인식 모듈
> - 피아노/기타 특화 전처리 알고리즘
> - 데이터 수집 및 레이블링 도구

> [!WARNING]
> **난이도 조정 알고리즘 (Phase 1)**
> 
> 악보를 "쉬운 버전"으로 변환하는 기능:
> 1. **템포 조정**: 연주 속도 50-150% 조절
> 2. **음표 단순화**: 16분음표 → 8분음표 등
> 3. **화음 단순화**: 복잡한 화음 → 기본 3화음
> 4. **옥타브 조정**: 음역대 축소 (피아노 전용)
> 5. **장식음 제거**: 트릴, 모르덴트 등 제거

---

## 🛠️ Proposed Changes

### Backend Components (Phase 1)

#### [NEW] [requirements.txt](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/requirements.txt)
Python 의존성 패키지:
- `oemer`: OMR 엔진
- `music21`: 음악 처리
- `flask`: 웹 서버
- `flask-cors`: CORS 처리
- `pillow`: 이미지 처리
- `numpy`: 수치 연산

#### [NEW] [app.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/app.py)
Flask 애플리케이션:
- `POST /api/upload`: 악보 이미지 업로드
- `POST /api/recognize`: OMR 처리
- `POST /api/play`: MIDI 생성
- `POST /api/simplify`: 난이도 조정
- `GET /api/download/<file_id>`: 파일 다운로드

#### [NEW] [omr_processor.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/omr_processor.py)
OMR 처리 모듈:
- `recognize_score(image_path)`: 악보 이미지 → MusicXML
- `preprocess_image()`: 이미지 전처리
- `validate_musicxml()`: 결과 검증

#### [NEW] [music_processor.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/music_processor.py)
음악 처리 모듈:
- `simplify_rhythm()`: 리듬 단순화
- `simplify_chords()`: 화음 단순화
- `adjust_tempo()`: 템포 조정
- `remove_ornaments()`: 장식음 제거
- `to_midi()`: MIDI 변환

---

### Frontend Components (Phase 1)

#### [NEW] [static/index.html](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/static/index.html)
메인 페이지:
- 악보 업로드 영역 (드래그 앤 드롭)
- 처리 옵션 선택 UI
- 악보 미리보기
- 재생 컨트롤

#### [NEW] [static/css/style.css](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/static/css/style.css)
프리미엄 UI 스타일:
- 다크 모드
- 글래스모피즘 효과
- 부드러운 애니메이션
- 반응형 디자인

#### [NEW] [static/js/app.js](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/static/js/app.js)
프론트엔드 로직:
- 파일 업로드 처리
- API 통신
- Tone.js 음악 재생
- VexFlow 악보 렌더링

---

### Additional Components

#### [NEW] [utils.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/utils.py)
유틸리티 함수:
- 파일 검증
- 임시 파일 관리
- 에러 핸들링

#### [NEW] [config.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/config.py)
설정:
- 업로드 경로
- 최대 파일 크기
- 지원 형식

#### [NEW] [README.md](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/README.md)
프로젝트 문서:
- 설치 방법
- 사용 방법
- API 문서
- 로드맵

---

### Future Components (Phase 2)

#### [NEW] [model_training/train.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/model_training/train.py)
모델 학습 스크립트:
- 데이터셋 로딩
- 모델 아키텍처 정의
- 학습 루프
- 체크포인트 저장

#### [NEW] [model_training/dataset.py](file:///c:/Users/SSAFY/Desktop/ai-score-pjt/model_training/dataset.py)
데이터셋 관리:
- 이미지 증강
- 레이블 처리
- 배치 생성

---

## ✅ Verification Plan

### Automated Tests

#### 1. Backend API 테스트
```bash
# 가상환경 생성
python -m venv venv
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python app.py
```

엔드포인트 테스트:
- `POST /api/upload`: 샘플 악보 업로드
- `POST /api/recognize`: OMR 처리
- `POST /api/simplify`: 난이도 조정

#### 2. OMR 기능 테스트
- 간단한 피아노 악보 인식
- 기타 악보 인식
- 스마트폰 촬영 이미지 인식

#### 3. 음악 재생 테스트
- MIDI 생성 및 재생
- 재생 컨트롤
- 템포 조정

---

### Manual Verification

#### UI/UX 테스트
- [ ] 드래그 앤 드롭 업로드
- [ ] 이미지 미리보기
- [ ] 로딩 애니메이션
- [ ] 악보 렌더링
- [ ] 다크 모드
- [ ] 모바일 반응형

#### 기능 테스트
- [ ] 원본 vs 단순화 악보 비교
- [ ] 템포 조정
- [ ] 파일 다운로드 (MusicXML, MIDI)

#### 에러 처리
- [ ] 잘못된 파일 형식
- [ ] 큰 파일 업로드
- [ ] 악보 아닌 이미지