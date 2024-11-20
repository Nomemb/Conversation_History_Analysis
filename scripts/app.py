import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import altair as alt

# 데이터 로드
file_path = '../dataset/6개월_상담데이터.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 와이드 레이아웃 설정
st.set_page_config(layout="wide")

# 날짜 형식 변환
df['상담일자시간'] = pd.to_datetime(df['상담일자시간'])

#########################################################################################

# 사이드바 커스텀 CSS
st.markdown(
    """
    <style>
    /* 사이드바 넓이 조정 */
    [data-testid="stSidebar"] {
        width: 100px;
        background-color: rgba(240, 240, 240, 0.7); /* 반투명 배경 */
    }

    /* 사이드바 내부 패딩 및 텍스트 조정 */
    [data-testid="stSidebar"] .css-1d391kg {
        padding: 5px;
        font-size: 8px;
        color: #333;
    }

    /* 사이드바 선택된 항목 스타일 */
    [data-testid="stSidebar"] .css-qrbaxs {
        font-weight: bold;
        color: #02ab21; /* 강조색 */
    }

    /* 옵션 메뉴 간 간격 조정 */
    [data-testid="stSidebar"] .css-1v3fvcr {
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 사이드바 구현
with st.sidebar:
    choose = option_menu(
        "LGU+ 관리자메뉴", 
        ["대시보드", "통화기록", "상담사 관리"],
        icons=['bar-chart-fill', 'cassette', 'people-fill'],
        menu_icon="person-fill-gear", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "deep pink", "font-size": "9px"}, 
            "nav-link": {"font-size": "10px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# 선택에 따라 동작 변경
if choose == "About":
    st.title("About")
    st.write("LGU+ 고객센터 관리자 모니터링 대시보드입니다.")
elif choose == "Photo Editing":
    st.title("Photo Editing")
    st.write("사진 편집 기능은 현재 준비 중입니다.")
elif choose == "Project Planning":
    st.title("Project Planning")
    st.write("프로젝트 계획 기능은 곧 제공될 예정입니다.")

# 대시보드 타이틀
st.title("LGU+ 고객센터 관리자 모니터링")
st.write("메인 화면")

###########################################################################################

# 데이터 전처리
df['상담일자'] = df['상담일자시간'].dt.date
min_date = df['상담일자'].min()
max_date = df['상담일자'].max()

# 전체 레이아웃 컨테이너
with st.container():
    st.markdown("## KPI 및 차트")
    
    # 첫 번째 줄: KPI
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric("총 상담 건수", f"{len(df):,}건")
    with kpi_col2:
        st.metric("IB 비율", f"{(df['ib/ob 구분'].value_counts().get('Inbound', 0) / len(df) * 100):.1f}%")
    with kpi_col3:
        st.metric("평균 상담 시간", f"{df['상담시간'].mean():.1f} 초")
    with kpi_col4:
        st.metric("고객 만족도 평균", f"{df['고객만족도'].mean():.1f} 점")

    # 두 번째 줄: 상담 분류별 건수, 월별 상담 건수
    row1_col1, row1_col2, row1_col3 = st.columns([1, 1, 1])
    with row1_col1:
        st.markdown("### 상담 분류별 상담 건수")
        category_counts = df['상담분류'].value_counts().reset_index()
        category_counts.columns = ['상담분류', '건수']

        category_chart = alt.Chart(category_counts).mark_bar().encode(
            x=alt.X('상담분류', sort='-y'),
            y='건수',
            color='상담분류'
        ).properties(width=400, height=300)
        st.altair_chart(category_chart)

    with row1_col2:
        st.markdown("### 월별 상담 건수")
        monthly_counts = df.groupby(df['상담일자시간'].dt.to_period('M')).size().reset_index(name='건수')
        monthly_chart = alt.Chart(monthly_counts).mark_line(point=True).encode(
            x=alt.X('상담일자시간:T'),
            y='건수',
            tooltip=['상담일자시간:T', '건수']
        ).properties(width=400, height=300)
        st.altair_chart(monthly_chart)

    with row1_col3:
        st.markdown("### 고객 만족도 분포")
        satisfaction_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('고객만족도:O', title='고객만족도'),
            y='count()',
            color='고객만족도:N'
        ).properties(width=400, height=300)
        st.altair_chart(satisfaction_chart)

    # 세 번째 줄: 고객 만족도, 상담사별 처리 건수
    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])
    with row2_col1:
        st.markdown("### 상담사별 처리 건수 Top 10")
        top_agents = df['상담자'].value_counts().head(10).reset_index()
        top_agents.columns = ['상담자', '건수']

        agent_chart = alt.Chart(top_agents).mark_bar().encode(
            x=alt.X('상담자', sort='-y'),
            y='건수',
            color='상담자'
        ).properties(width=400, height=300)
        st.altair_chart(agent_chart)

    with row2_col2:
        st.markdown("### 지역별 상담 분포")
        region_counts = df['지역'].value_counts().reset_index()
        region_counts.columns = ['지역', '건수']

        region_chart = alt.Chart(region_counts).mark_bar().encode(
            x=alt.X('지역', sort='-y'),
            y='건수',
            color='지역'
        ).properties(width=400, height=300)
        st.altair_chart(region_chart)

    # 다섯 번째 줄: 공지사항
    with row2_col3:
        st.markdown("### 공지사항")
        st.info(
            """
            - 고객 만족도를 높이기 위해 매월 상담 교육 세션이 진행됩니다.
            - 다음 교육 일정: **2024년 12월 10일**
            """
        )
