import streamlit as st
import pandas as pd
import altair as alt


# 데이터 로드
'''
@st.cache
def load_data():
    file_path = "C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/6개월_상담데이터"  # 방금 생성한 CSV 파일 경로
    return pd.read_csv(file_path)

df = load_data()
'''

file_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/6개월_상담데이터.csv'
df = pd.read_csv(file_path, encoding='utf-8')



# 날짜 형식 변환
df['상담일자시간'] = pd.to_datetime(df['상담일자시간'])

# 대시보드 레이아웃
st.title("통신사 고객센터 상담 대시보드")

# KPI 섹션
st.markdown("### 상담 KPI")
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 상담 건수", f"{len(df):,}건")
col2.metric("Inbound 비율", f"{(df['ib/ob 구분'].value_counts()['Inbound'] / len(df) * 100):.1f}%")
col3.metric("평균 상담 시간", f"{df['상담시간'].mean():.1f} 초")
col4.metric("고객 만족도 평균", f"{df['고객만족도'].mean():.1f} 점")

# 상담 분류별 건수 시각화
st.markdown("### 상담 분류별 상담 건수")
category_counts = df['상담분류'].value_counts().reset_index()
category_counts.columns = ['상담분류', '건수']

chart = alt.Chart(category_counts).mark_bar().encode(
    x=alt.X('상담분류', sort='-y'),
    y='건수',
    color='상담분류'
)
st.altair_chart(chart, use_container_width=True)

# 월별 상담 건수 시각화
st.markdown("### 월별 상담 건수")
df['월'] = df['상담일자시간'].dt.to_period('M')
monthly_counts = df.groupby('월').size().reset_index(name='건수')

line_chart = alt.Chart(monthly_counts).mark_line(point=True).encode(
    x='월:T',
    y='건수',
    color=alt.value("#5276A7"),
    tooltip=['월:T', '건수']
)
st.altair_chart(line_chart, use_container_width=True)

# 고객 만족도 분포
st.markdown("### 고객 만족도 분포")
satisfaction_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('고객만족도:O', title='고객만족도'),
    y='count()',
    color='고객만족도:N'
)
st.altair_chart(satisfaction_chart, use_container_width=True)

# 상담사별 처리 건수
st.markdown("### 상담사별 처리 건수 Top 10")
top_agents = df['상담자'].value_counts().head(10).reset_index()
top_agents.columns = ['상담자', '건수']

bar_chart_agents = alt.Chart(top_agents).mark_bar().encode(
    x=alt.X('상담자', sort='-y'),
    y='건수',
    color='상담자'
)
st.altair_chart(bar_chart_agents, use_container_width=True)

# 지역별 상담 분포
st.markdown("### 지역별 상담 건수")
region_counts = df['지역'].value_counts().reset_index()
region_counts.columns = ['지역', '건수']

region_chart = alt.Chart(region_counts).mark_bar().encode(
    x=alt.X('지역', sort='-y'),
    y='건수',
    color='지역'
)
st.altair_chart(region_chart, use_container_width=True)

# 공지사항 영역 (임의 데이터)
st.markdown("### 공지사항")
st.info("고객 만족도를 높이기 위해 매월 상담 교육 세션이 진행됩니다. 다음 교육은 2024년 12월 10일입니다.")

# 상단 키워드 클라우드 섹션은 외부 라이브러리 필요 (wordcloud) - 필요시 별도 구현 가능
