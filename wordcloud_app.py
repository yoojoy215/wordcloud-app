"""
한글 기사 워드 클라우드 생성기 - Streamlit UI
사용자가 기사 URL을 입력하면 자동으로 워드 클라우드 생성
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from kiwipiepy import Kiwi
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="한글 기사 워드 클라우드",
    page_icon="📰",
    layout="wide"
)

# 한글 폰트 설정
import platform
import os

def get_font_path():
    """OS에 맞는 한글 폰트 경로 반환"""
    system = platform.system()
    
    if system == 'Windows':
        return 'C:/Windows/Fonts/malgun.ttf'
    elif system == 'Darwin':  # macOS
        return '/System/Library/Fonts/Arial Unicode.ttf'
    else:  # Linux
        possible_paths = [
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

# 폰트 설정
font_path = get_font_path()
if font_path and os.path.exists(font_path):
    plt.rcParams['font.family'] = 'DejaVu Sans'
else:
    # 폰트를 찾을 수 없으면 기본값 사용
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']

plt.rcParams['axes.unicode_minus'] = False

# ============ 함수 정의 ============

@st.cache_data
def get_latest_article_from_homepage(homepage_url):
    """중앙일보 메인 페이지에서 최신 기사 URL 추출"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(homepage_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 중앙일보 최신 기사 찾기
        if 'joongang' in homepage_url.lower():
            # 링크에서 /article/ 패턴 찾기
            article_links = soup.find_all('a', href=True)
            for link in article_links:
                href = link.get('href', '')
                if '/article/' in href and href.startswith('/'):
                    article_url = f"https://www.joongang.co.kr{href}"
                    return article_url
                elif '/article/' in href and href.startswith('http'):
                    return href
        
        # 조선일보
        elif 'chosun' in homepage_url.lower():
            article_links = soup.find_all('a', href=True)
            for link in article_links:
                href = link.get('href', '')
                if '/article/' in href and href.startswith('http'):
                    return href
        
        # 동아일보
        elif 'donga' in homepage_url.lower():
            article_links = soup.find_all('a', href=True)
            for link in article_links:
                href = link.get('href', '')
                if '/article/' in href:
                    if href.startswith('http'):
                        return href
                    elif href.startswith('/'):
                        return f"https://www.donga.com{href}"
        
        return None
        
    except Exception as e:
        return None

def normalize_url(url):
    """URL 정규화 - 메인 페이지면 최신 기사로 변환"""
    url = url.strip()
    
    # 메인 페이지 패턴 감지
    is_homepage = (
        url.endswith('/') or 
        url.endswith('joongang.co.kr') or 
        url.endswith('chosun.com') or
        url.endswith('donga.com') or
        'www.joongang.co.kr' in url and '/article/' not in url
    )
    
    if is_homepage:
        # 최신 기사 추출
        article_url = get_latest_article_from_homepage(url if url.startswith('http') else f"https://{url}")
        if article_url:
            return article_url, "메인 페이지에서 최신 기사로 자동 변환됨"
        else:
            return url, "최신 기사를 찾을 수 없었습니다. 기사 URL을 직접 입력해주세요."
    
    return url, None

@st.cache_data
def scrape_article(url):
    """기사 크롤링"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 제목 추출 (여러 패턴 시도)
        title_elem = (soup.find('h1', class_='headline') or 
                     soup.find('h1', class_='title') or
                     soup.find('h1', class_='article_title') or
                     soup.find('h2', class_='title') or
                     soup.find('h1') or
                     soup.find('title'))
        title = title_elem.text.strip() if title_elem else "제목 없음"
        
        # 본문 추출 (여러 패턴 시도)
        article_body = (soup.find('div', {'id': 'article_body'}) or
                       soup.find('div', class_='article_body') or
                       soup.find('div', class_='article-body') or
                       soup.find('div', class_='article_text') or
                       soup.find('div', class_='content_body') or
                       soup.find('article') or
                       soup.find('div', class_='content'))
        
        if article_body:
            paragraphs = article_body.find_all('p')
            content = ' '.join([p.text.strip() for p in paragraphs if p.text.strip()])
        else:
            # 모든 p 태그 수집 (100자 이상만)
            paragraphs = soup.find_all('p')
            content = ' '.join([p.text.strip() for p in paragraphs if len(p.text.strip()) > 50])
        
        # 내용이 비어있으면 에러
        if not content or len(content) < 100:
            return title, "error: 기사 본문을 찾을 수 없습니다. 개별 기사 URL을 입력해주세요 (메인 페이지 제외)"
        
        return title, content
        
    except requests.exceptions.Timeout:
        return None, "error: 요청 시간 초과 (연결 문제)"
    except requests.exceptions.ConnectionError:
        return None, "error: 연결 실패"
    except Exception as e:
        return None, f"error: {str(e)}"

@st.cache_resource
def get_kiwi():
    """Kiwi 초기화 (캐싱)"""
    return Kiwi()

def analyze_morphemes(text, top_n=50):
    """형태소 분석 및 명사 추출"""
    kiwi = get_kiwi()
    
    # 형태소 분석
    result = kiwi.analyze(text)
    
    # 명사만 추출
    nouns = []
    for token_result in result:
        for morph in token_result[0]:
            if morph.tag in ['NNG', 'NNP']:
                if len(morph.form) > 1:
                    nouns.append(morph.form)
    
    # 빈도 계산
    noun_counts = Counter(nouns)
    
    return noun_counts

def remove_stopwords(noun_counts, custom_stopwords=None):
    """불용어 제거"""
    default_stopwords = [
        '기자', '뉴스', '사진', '연합뉴스', '중앙일보', '동아일보',
        '조선일보', '한겨레', '경향신문', '이데일리', '뉴시스',
        '것', '수', '등', '때', '년', '월', '일', '시', '분',
        '대한민국', '서울', '한국', '우리', '저희', '관련',
        '제공', '무단', '전재', '재배포', '금지', '저작권자'
    ]
    
    if custom_stopwords:
        default_stopwords.extend(custom_stopwords)
    
    filtered_nouns = {
        word: count for word, count in noun_counts.items()
        if word not in default_stopwords
    }
    
    return filtered_nouns

def create_wordcloud(word_freq, width=1200, height=800, colormap='viridis'):
    """워드 클라우드 생성"""
    if not word_freq:
        return None
    
    font_path_to_use = get_font_path()
    
    wc = WordCloud(
        font_path=font_path_to_use if font_path_to_use and os.path.exists(font_path_to_use) else None,
        width=width,
        height=height,
        background_color='white',
        max_words=100,
        relative_scaling=0.3,
        colormap=colormap
    ).generate_from_frequencies(word_freq)
    
    return wc

# ============ UI 구성 ============

# 헤더
st.title("📰 한글 기사 워드 클라우드 생성기")
st.markdown("---")
st.markdown("""
### 사용 방법
1. 중앙일보 메인 페이지 또는 개별 기사 URL을 입력하세요
2. '분석 시작' 버튼을 클릭하세요
3. 워드 클라우드가 자동으로 생성됩니다!

**지원 사이트:** 중앙일보, 조선일보, 동아일보, 한겨레, 경향신문 등 대부분의 한글 뉴스 사이트

✨ **특징:** 메인 페이지(https://www.joongang.co.kr/)를 입력하면 최신 기사로 자동 변환됩니다!
""")

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # URL 입력
    default_url = "https://www.joongang.co.kr/" 
    article_url = st.text_input(
        "기사 URL",
        value=default_url,
        placeholder="https://..."
    )
    
    st.caption("💡 팁: 중앙일보 메인 페이지를 입력하면 최신 기사로 자동 변환됩니다!")
    
    # 고급 설정
    st.subheader("고급 설정")
    
    top_n = st.slider("표시할 단어 개수", 10, 100, 50)
    
    custom_stopwords_input = st.text_area(
        "추가 불용어 (쉼표로 구분)",
        placeholder="예: 단어1, 단어2, 단어3"
    )
    
    custom_stopwords = [w.strip() for w in custom_stopwords_input.split(',') if w.strip()]
    
    colormap = st.selectbox(
        "색상 테마",
        ['viridis', 'plasma', 'inferno', 'magma', 'cool', 'hot', 'spring', 'summer', 'autumn', 'winter']
    )
    
    analyze_button = st.button("🔍 분석 시작", use_container_width=True, type="primary")

# 메인 영역
col1, col2 = st.columns([1, 1])

if analyze_button:
    if not article_url:
    if not article_url:
        st.error("❌ URL을 입력해주세요!")
    else:
        # URL 정규화 (메인 페이지면 최신 기사로 변환)
        with st.spinner('URL 확인 중...'):
            normalized_url, conversion_msg = normalize_url(article_url)
        
        if conversion_msg:
            if "자동 변환" in conversion_msg:
                st.info(f"✅ {conversion_msg}")
            else:
                st.warning(f"⚠️ {conversion_msg}")
        
        if normalized_url != article_url:
            article_url = normalized_url
        
        # 기사 크롤링
        with st.spinner('기사 수집 중...'):
            title, content = scrape_article(article_url)
        
        if content and not content.startswith("error"):
            # 기사 정보 표시
            with col1:
                st.subheader("📄 기사 정보")
                st.markdown(f"**제목:** {title}")
                st.markdown(f"**본문 길이:** {len(content):,}자")
                
                with st.expander("본문 미리보기"):
                    st.text(content[:500] + "..." if len(content) > 500 else content)
            
            # 형태소 분석
            with st.spinner('형태소 분석 중...'):
                noun_counts = analyze_morphemes(content, top_n)
                filtered_nouns = remove_stopwords(noun_counts, custom_stopwords)
            
            # 상위 명사 표시
            with col2:
                st.subheader(f"📊 상위 {min(top_n, len(filtered_nouns))}개 명사")
                
                top_nouns = dict(sorted(filtered_nouns.items(), key=lambda x: x[1], reverse=True)[:top_n])
                
                # 데이터프레임으로 표시
                import pandas as pd
                df_nouns = pd.DataFrame(list(top_nouns.items()), columns=['명사', '빈도'])
                df_nouns.index = range(1, len(df_nouns) + 1)
                st.dataframe(df_nouns, use_container_width=True, height=400)
            
            # 워드 클라우드 생성
            st.markdown("---")
            st.subheader("☁️ 워드 클라우드")
            
            with st.spinner('워드 클라우드 생성 중...'):
                # colormap 업데이트
                wc = create_wordcloud(filtered_nouns, width=1400, height=700, colormap=colormap)
                
                if wc:
                    fig, ax = plt.subplots(figsize=(16, 8))
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title(f'워드 클라우드: {title}', fontsize=16, fontweight='bold', pad=20)
                    plt.tight_layout()
                    
                    st.pyplot(fig)
                    
                    # 다운로드 버튼
                    buf = BytesIO()
                    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                    buf.seek(0)
                    
                    st.download_button(
                        label="💾 워드 클라우드 다운로드",
                        data=buf,
                        file_name=f"wordcloud_{title[:20]}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.error("워드 클라우드를 생성할 수 없습니다.")
            
            st.success("✅ 분석 완료!")
            
        else:
            error_msg = content if content else '알 수 없음'
            if "error:" in error_msg:
                error_msg = error_msg.replace("error: ", "")
            st.error(f"❌ 기사를 가져올 수 없습니다.\n\n📝 {error_msg}\n\n💡 개별 기사 URL을 입력했는지 확인해주세요. (메인 페이지 제외)")

else:
    # 초기 화면
    st.info("👈 왼쪽 사이드바에서 URL을 입력하고 '분석 시작' 버튼을 눌러주세요!")
    
    # 예시 이미지나 설명
    st.markdown("""
    ### ✨ 주요 기능
    
    - 🌐 **다양한 뉴스 사이트 지원**: 중앙일보, 조선일보, 동아일보, 한겨레 등 대부분의 한글 뉴스 사이트
    - 🔍 **정확한 형태소 분석**: Kiwi 형태소 분석기 사용
    - 🎨 **커스터마이징**: 색상, 단어 개수, 불용어 설정 가능
    - 💾 **다운로드**: 고해상도 PNG로 저장
    
    ### 📌 팁
    - **개별 기사 URL**을 입력해야 합니다 (메인 페이지 X)
    - 더 정확한 결과를 위해 불용어를 추가해보세요
    - 다양한 색상 테마를 시도해보세요
    - 단어 개수를 조정하여 원하는 수준의 상세도를 얻으세요
    
    ### 🔗 기사 URL 예시
    - ✅ https://www.joongang.co.kr/article/25398258
    - ✅ https://www.chosun.com/article/60012345
    - ❌ https://www.joongang.co.kr/ (메인 페이지)
    """)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Made with ❤️ using Streamlit & Kiwi</p>
</div>
""", unsafe_allow_html=True)