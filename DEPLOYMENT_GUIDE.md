# 배포 가이드

## Streamlit Cloud 배포 (추천 - 무료)

### 1단계: GitHub에 업로드
```bash
# 저장소 초기화
git init
git add .
git commit -m "Initial commit: wordcloud app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/wordcloud-app.git
git push -u origin main
```

### 2단계: Streamlit Cloud에서 배포
1. https://share.streamlit.io 방문
2. "Deploy an app" 클릭
3. GitHub 계정 연결
4. 저장소 선택: `YOUR_USERNAME/wordcloud-app`
5. 메인 파일: `wordcloud_app.py`
6. 배포 시작

**배포 완료 후 URL**: `https://YOUR_USERNAME-wordcloud-app.streamlit.app`

---

## 로컬에서 테스트

### 필수 요구사항
- Python 3.8+

### 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/YOUR_USERNAME/wordcloud-app.git
cd wordcloud-app

# 2. 가상 환경 생성 (선택사항 하지만 권장)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. 의존 패키지 설치
pip install -r requirements.txt

# 4. 앱 실행
streamlit run wordcloud_app.py
```

브라우저가 자동으로 `http://localhost:8501`로 열립니다.

---

## 트러블슈팅

### Kiwi 초기화 시간 오래 걸림
- 첫 실행 시 Kiwi 형태소 분석기 초기화에 1-2분 소요
- 이후는 캐시되어 빠름

### 한글 폰트 깨짐 (Linux)
```bash
# 한글 폰트 설치
sudo apt-get install fonts-noto-cjk
```

### 웹 크롤링 오류
- 일부 뉴스 사이트는 웹 크롤링을 차단할 수 있음
- User-Agent를 통해 우회 시도함
- 개별 기사 URL이 정상인지 확인

### Streamlit Cloud에서 timeout
- Kiwi 초기화로 인한 콜드 스타트 시간 초과 가능
- 첫 실행 후는 정상 작동

---

## 환경 변수 설정

Streamlit Cloud 배포 시 보안이 필요한 경우:

1. 저장소의 Settings → Secrets
2. 필요한 환경 변수 추가

예: API 키, 인증 정보 등

---

## 성능 최적화

### 캐싱
- `@st.cache_data`: 기사 크롤링 결과 캐시
- `@st.cache_resource`: Kiwi 인스턴스 캐시

### 메모리 사용
- 한 번에 하나의 기사만 처리
- 큰 이미지는 필요시만 생성

---

## 문제 보고
GitHub Issues에서 보고해주세요: https://github.com/YOUR_USERNAME/wordcloud-app/issues

---

## 라이선스
MIT License
