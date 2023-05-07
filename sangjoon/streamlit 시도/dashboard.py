#스트림릿 라이브러리를 사용하기 위한 임포트
#pip install matplotlib
#pip install plotly.express
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import datetime
#1.terminal을 열고 %pip install streamlit을 쳐줍니다.
#2. 설치가 다 되면 streamlit run app.py를 쳐줍니다. (여기서 app.py는 폴더안에 새로 만든 python 형식 파일입니다.)
#3.Email 칸에서 빈칸으로 엔터를 쳐 주시고 아래 URL, Network URL 주소를 복사해줍니다.
#4. 파이썬 파일을 수정하고 저장하고 난 후 URL창에서 새로고침을 눌러주면 해당 코드에 대한 내용이 나옵니다.
import matplotlib.font_manager as fm
font_path = '/home/ubuntu/newnew/NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path)



def main():
    #df변수에 csv파일을 로드해줍니다.(csv파일이름에 따라 변경)
    df= pd.read_csv('dash.csv')
    st.title("스킨케어 코스메틱 브랜드 리뷰데이터 감성분석")
    
        #시각화를 진행합니다.
    #부제목을 달아줍니다.
    #1. 별점 데이터 프레임 개수 그래프로 확인.(1,2,3,4,5,6)
    # 닥터지가 제일 많은 비율을 차지하고 있는것을 확인.    
    st.subheader('#브랜드별 리뷰 데이터 분포')
    fig1=px.pie(df, 'brand_name', 'stars_updated')
    st.plotly_chart(fig1)
    
    st.subheader('각 브랜드별 별점 분포')
    fig11, ax = plt.subplots(figsize=(12,8))

    # 브랜드 이름 추출
    brand_names = df.brand_name.unique()

    # 색상 설정
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    # 막대 너비
    bar_width = 0.1

    # 그래프 그리기
    for i, star in enumerate([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]):
        data = []
        for brand in brand_names:
            data.append(len(df[(df.brand_name == brand) & (df.stars_updated == star)]))
        x = np.arange(len(data))
        b = ax.bar(x + i * bar_width, data, bar_width, color=colors[i], label=str(star) + " stars")
        
    # 축과 레이블 설정
    ax.set_xticks(x + bar_width * 2.5)
    ax.set_xticklabels(brand_names,fontproperties=fontprop)
    ax.legend()

    # 그래프 출력
    st.pyplot(fig11)


    
    
    #사이드바에 담을 항목들을 만들어줍니다.
    st.sidebar.title('품목구분')
    st.sidebar.checkbox('올리브영')
    select_multi_species = st.sidebar.multiselect(
        '확인하고 싶은 브랜드를 선택하세요. 복수선택가능',
        ['닥터지','라운드랩','라네즈','아이소이','아누아','에스트라']
        )
    tmp_df = df[df['brand_name'].isin(select_multi_species)]
    st.table(tmp_df.head())
    
    radio_select = st.sidebar.radio(
        "what is key colum?",
        ['stars_updated'],
        horizontal=True
    )
    
    slider_range = st.sidebar.slider(
        '범위를 골라주세요.',
        0.0,
        6.0,
        (2.0, 5.0)
    )
    
    start_button = st.sidebar.button(
        "filter apply"
    )
    #버튼이 눌리는 경우 start_button 값을 True로 두고 uf 문으로 버튼을 눌렀을때를 구현.
    if start_button:
            tmp_df = df[df['brand_name'].isin(select_multi_species)]
            #slider input으로 받은 값에 해당하는 값을 기준으로 데이터를 필터링합니다.
            tmp_df= tmp_df[ (tmp_df[radio_select] >= slider_range[0]) & (tmp_df[radio_select] <= slider_range[1])]
            st.table(tmp_df)
            # 성공문구 
            st.sidebar.success("Filter Applied!")
            
    #스케일링을 끝낸 데이터 프레임
    
    # 데이터 로딩
    df1 = pd.read_csv('final_df3.csv')
    df2 = pd.read_csv('final_df3.csv')
    # 1
    # 데이터 불러오기
    # Filter data for 2022-2023 reviews only
    # 2022년과 2023년 리뷰 추출
    df2 = df2[df2['review_year'].isin([2022, 2023])]

    st.subheader('2022-2023 년도 브랜드별, 날짜별 리뷰개별점수')
        # 2
    # 브랜드 선택 옵션
    # 2022년과 2023년 리뷰 추출
    # Convert review_year and review_month to datetime
    df2['date'] = pd.to_datetime(df2['review_year'].astype(int).astype(str) + '/' + df2['review_month'].astype(int).astype(str))

    # 브랜드 리스트를 만들어줍니다.
    brands = sorted(df2['brand_name'].unique())

    # 연도 리스트를 만들어줍니다.
    years = sorted(df2['review_year'].unique())

    # 월 리스트를 만들어줍니다.
    months = sorted(df2['review_month'].unique())

    # 사이브 바에 브랜드와 날짜를 고를 수 있게 만들어줍니다.
    selected_brands = st.sidebar.multiselect('Select Brands', brands, default=brands)
    start_year, end_year = st.sidebar.select_slider('Select Year Range', options=years, value=(years[0], years[-1]))
    start_month, end_month = st.sidebar.select_slider('Select Month Range', options=months, value=(months[0], months[-1]))

    # 선택에 맞게 필터를 만들어줍니다.
    mask = (
        df2['brand_name'].isin(selected_brands) &
        (df2['review_year'] >= start_year) & (df2['review_year'] <= end_year) &
        (df2['review_month'] >= start_month) & (df2['review_month'] <= end_month)
    )
    filtered_df = df2.loc[mask]

    # 라인차트에 필터링을 추가해줍니다.
    line_chart = alt.Chart(filtered_df).mark_line().encode(
        x='date:T',
        y='total_score:Q',
        color='brand_name:N'
    ).properties(
        width=1000,
        height=600
    )

 
    # 라인차트를 나타냅니다.
    st.altair_chart(line_chart)
    
    
    
    
     # brand_name 칼럼 값 추출
    brands = df2['brand_name'].unique()
    # 시각화
    st.subheader('2022-2023 년도 브랜드별 리뷰')
    brand_selected = st.selectbox('브랜드 선택', brands)

    if brand_selected:
        # 선택한 브랜드의 데이터 추출
        brand_data = df2[df2['brand_name']==brand_selected]
        
        # review_month로 그룹화하여 total_score 계산
        monthly_scores = brand_data.groupby('review_month')['total_score'].mean()
        
        # 막대 그래프 시각화
        fig, ax = plt.subplots()
        ax.bar(monthly_scores.index, monthly_scores.values)
        ax.set_xlabel('월',fontproperties=fontprop)
        ax.set_ylabel('평균 total_score',fontproperties=fontprop)
        ax.set_title(f'{brand_selected} 브랜드 2022-2023 년도 월별 평균 total_score',fontproperties=fontprop)
        st.pyplot(fig)
        
    
if __name__ == '__main__' :
    main()