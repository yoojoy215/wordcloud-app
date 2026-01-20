# 한글 기사 워드 클라우드 생성기

한글 뉴스 기사에서 자동으로 워드 클라우드를 생성하는 Streamlit 웹 애플리케이션입니다.

## ✨ 주요 기능

- 🌐 **다양한 뉴스 사이트 지원**: 중앙일보, 조선일보, 동아일보, 한겨레 등
- 🔄 **자동 URL 변환**: 메인 페이지를 입력하면 최신 기사로 자동 변환
- 🔍 **정확한 형태소 분석**: Kiwi 형태소 분석기로 명사 추출
- 🎨 **커스터마이징**: 색상, 단어 개수, 불용어 설정 가능
- 💾 **고해상도 다운로드**: PNG 형식으로 저장 가능

## 📋 사용 방법

1. **URL 입력**
   - 중앙일보 메인 페이지: `https://www.joongang.co.kr/`
   - 또는 개별 기사 URL: `https://www.joongang.co.kr/article/25398258`

2. **고급 설정** (선택사항)
   - 표시할 단어 개수 조절
   - 불용어 추가
   - 색상 테마 선택

3. **분석 시작** 버튼 클릭

4. **결과 확인**
   - 기사 제목, 본문 길이
   - 상위 명사 빈도
   - 워드 클라우드 이미지
   - PNG 다운로드

## 🚀 온라인 배포 (권장)

**[🌐 온라인 데모 - 클릭해서 지금 사용하기](https://wordcloud-app.streamlit.app)**

Streamlit Cloud에서 무료로 호스팅됩니다. 설치 없이 바로 사용 가능합니다!

---

## 💻 로컬 실행

```bash
# 1. 저장소 클론
git clone https://github.com/yoojoy215/wordcloud-app.git
cd wordcloud-app

# 2. 의존 패키지 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run wordcloud_app.py
```

브라우저가 자동으로 열리며, `http://localhost:8501`에서 접속 가능합니다.

## 📦 설치 요구사항

- Python 3.11+
- 의존 패키지는 `requirements.txt` 참조

## 🔧 기술 스택

- **Streamlit**: 웹 프레임워크
- **BeautifulSoup**: HTML 파싱
- **Kiwi**: 한글 형태소 분석
- **WordCloud**: 워드 클라우드 생성
- **Matplotlib**: 데이터 시각화

## 📝 기본 설정

### 한글 폰트
Windows에서는 자동으로 Malgun Gothic을 사용합니다.

### 불용어 (기본)
다음 단어들은 자동으로 제외됩니다:
- 신문사: 기자, 뉴스, 중앙일보, 조선일보, 동아일보, 한겨레, 경향신문, 이데일리, 뉴시스
- 일반: 사진, 제공, 무단, 전재, 재배포, 금지, 저작권자

### 색상 테마
10가지 색상 테마 지원:
- viridis, plasma, inferno, magma
- cool, hot, spring, summer, autumn, winter

## 🐛 문제 해결

### 한글이 깨져요
Windows: 자동으로 Malgun Gothic 사용 (설치 필요 없음)
Linux: `sudo apt-get install fonts-noto-cjk` 설치 필요
macOS: 자동으로 시스템 폰트 사용

### 기사를 못 찾아요
- 개별 기사 URL을 확인하세요
- 메인 페이지인 경우, 자동으로 최신 기사로 변환됩니다

### 속도가 느려요
- 첫 실행 시 Kiwi 초기화에 시간이 걸립니다
- Streamlit 캐싱 덕분에 같은 기사는 빠르게 로드됩니다

## 🌐 온라인 배포

### Streamlit Cloud (추천 - 무료)

더 자세한 배포 가이드는 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 참조하세요.

**배포 절차:**
1. GitHub에 이 저장소를 Fork/Upload
2. https://share.streamlit.io 방문
3. GitHub 저장소 선택 후 배포

**배포 URL 형식**: `https://[YOUR_USERNAME]-wordcloud-app.streamlit.app`

## 📊 예시 결과

입력: 중앙일보 메인 페이지 또는 개별 기사 URL
출력: 기사의 핵심 단어를 시각적으로 나타낸 워드 클라우드

## 📄 라이선스

MIT License

## 👨‍💻 만든이

MS DataSchool 프로젝트

---

**배포 준비 완료!** GitHub에 push한 후 Streamlit Cloud에서 배포하세요.

**문제가 있으신가요?** [Issues](https://github.com/yoojoy215/wordcloud-app/issues) 페이지에서 보고해주세요!
