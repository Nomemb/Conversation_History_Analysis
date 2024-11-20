import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import altair as alt
import my_sql

# 데이터 로드
file_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/6개월_상담데이터.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 와이드 레이아웃 설정
st.set_page_config(layout="wide")

# 날짜 형식 변환
df['상담일자시간'] = pd.to_datetime(df['상담일자시간'])

#########################################################################################

st.markdown(
    """
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

# 사이드바 CSS 커스텀
st.markdown(
    """
    <style>
    /* 사이드바 넓이 조정 */
    [data-testid="stSidebar"] {
        width: 100px;
        background-color: rgba(240, 240, 240, 0.7); /* 반투명 배경 */
    }

    /* 사이드바 내부 패딩 및 텍스트 조정 */
    [data-testid="stSidebar"] .css-18e3th9 {
        margin-top:0px;
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

# 첫 번째 사이드바 블록
with st.sidebar:
    st.markdown("### **메뉴**")
    choose_1 = option_menu(
        "", 
        ["대시보드", "통화기록", "상담사 관리", "상담사 일정 관리", "설정"],
        icons=['bar-chart-fill', 'headphones', 'people-fill', 'calendar-check', 'gear-fill'],
        menu_icon="person-fill-gear", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "deep pink", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# 세번째 사이드바 블록
with st.sidebar:
    st.markdown("### **관리**")
    choose_2 = option_menu(
        "", 
        ["로그 분석", "레포트 관리", "회의 일정 관리", "VOC 관리", "지원"],
        icons=['graph-up', 'file-earmark-text', 'calendar-check', 'folder', 'info-circle'],
        menu_icon="list-ul", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "blue", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0288d1"},
        }
    )

# 두 번째 사이드바 블록
with st.sidebar:
    st.markdown("### **이동**")
    choose_3 = option_menu(
        "", 
        ["유플러스닷컴", "고객센터 페이지", "공식 온라인 스토어", "LGU+ 그룹웨어", "지원"],
        icons=['house', 'house', 'house', 'house', 'house'],
        menu_icon="list-ul", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "red", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0288d1"},
        }
    )



# 대시보드 타이틀
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h1 style="margin-right: 20px; margin-top: -80px;">LGU+ 고객센터 관리자 모니터링</h1>
    </div>
    """, 
    unsafe_allow_html=True
)



###########################################################################################

# 데이터 전처리
df['상담일자'] = df['상담일자시간'].dt.date
min_date = df['상담일자'].min()
max_date = df['상담일자'].max()

# 전체 레이아웃 컨테이너
with st.container():
    col1, col2 = st.columns([2, 8])  # 비율을 조정하여 타이틀과 KPI 너비를 설정
    with col1:
        st.markdown(
            """
            <h1 style="font-family: 'Arial'; font-size: 36px; text-align: center; color: #e6007e;">2팀 KPI</h1>
            """, 
            unsafe_allow_html=True
        )  # 타이틀 폰트 수정 및 가운데 정렬
    with col2:
        # 각 메트릭을 담을 박스 스타일 설정
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 15px; padding: 5px 10px 3px 10px; text-align: center;">
                    <h4>총 상담 건수</h4>
                    <p style="font-size: 16px; color: #333;">{:,} 건</p>
                </div>
                """.format(len(df)),
                unsafe_allow_html=True
            )
        with kpi_col2:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 15px; padding: 5px 10px 3px 10px; text-align: center;">
                    <h4>IB 비율</h4>
                    <p style="font-size: 18px; color: #333;">{:.1f}%</p>
                </div>
                """.format((df['ib/ob 구분'].value_counts().get('Inbound', 0) / len(df) * 100)),
                unsafe_allow_html=True
            )
        with kpi_col3:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 15px; padding: 5px 10px 3px 10px; text-align: center;">
                    <h4>평균 상담 시간</h4>
                    <p style="font-size: 18px; color: #333;">{:.1f} 초</p>
                </div>
                """.format(df['상담시간'].mean()),
                unsafe_allow_html=True
            )
        with kpi_col4:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 15px; padding: 5px 10px 3px 10px; text-align: center;">
                    <h4>고객 만족도 평균</h4>
                    <p style="font-size: 18px; color: #333;">{:.1f} 점</p>
                </div>
                """.format(df['고객만족도'].mean()),
                unsafe_allow_html=True
            )



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
        ).properties(width=450, height=300)
        st.altair_chart(category_chart)

    with row1_col2:
        st.markdown("### 월별 상담 건수")
        monthly_counts = df.groupby(df['상담일자시간'].dt.to_period('M')).size().reset_index(name='건수')
        monthly_chart = alt.Chart(monthly_counts).mark_line(point=True).encode(
            x=alt.X('상담일자시간:T'),
            y='건수',
            tooltip=['상담일자시간:T', '건수']
        ).properties(width=450, height=300)
        st.altair_chart(monthly_chart)

    with row1_col3:
        st.markdown("### 고객 만족도 분포")
        satisfaction_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('고객만족도:O', title='고객만족도'),
            y='count()',
            color='고객만족도:N'
        ).properties(width=450, height=300)
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
        ).properties(width=450, height=300)
        st.altair_chart(agent_chart)

    with row2_col2:
        st.markdown("### 지역별 상담 분포")
        region_counts = df['지역'].value_counts().reset_index()
        region_counts.columns = ['지역', '건수']

        region_chart = alt.Chart(region_counts).mark_bar().encode(
            x=alt.X('지역', sort='-y'),
            y='건수',
            color='지역'
        ).properties(width=450, height=300)
        st.altair_chart(region_chart)

    # 다섯 번째 줄: 공지사항
    with row2_col3:
        st.markdown("### 공지사항")
        st.info(
            """
            - [교육] 24년 12월 정규 교육 안내
            - [인사] 24년 하반기 KPI 공지
            - [마케팅] 12월 프로모션 관련 안내
            """
        )