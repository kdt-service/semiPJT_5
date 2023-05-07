import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

 brand_data = df.loc[(df['stars_updated'] == option)]
    brand_data = brand_data[brand_data.columns.difference(['goodsNo', 'gdasCont', 'goodsNm', 'dispRegDate','gdasSeq','subcategory','reviwerMbrNo','gasScrval','stars','five_stars_split','brand_name','stars_updated'])]
    b_index = brand_data.index.tolist()
    st.area_chart(brand_data.loc[b_index[0]], use_container_width=True)
    
    
import pandas as pd

def bring_test_2023_data():
    
    df = pd.read_csv("oliveyoung_labeled.csv")
    df = df[df['brand_name'] == '닥터지'].copy() # 닥터지 데이터만 가져와서 테스트
    df['review_date'] = pd.to_datetime(df['dispRegDate']) # review_date로 datetime화
    
    # year,month 구분 컬럼 생성
    df['review_year'] = df['review_date'].dt.year
    df['review_month'] = df['review_date'].dt.month
    # 23년도 데이터로 테스트
    df = df[df['review_year'].isin([2023])].copy() 
    
    return df

# 필요한 Dropdown 리스트, Checklist 리스트 가져오기
def bring_needed_list(df):
    # Dropdown에 쓰일 year_list
    year_list = df['review_date'].dt.year.unique().tolist()
    year_list = sorted(year_list)
    # Dropdown에 쓰일 month_list
    month_list = df['review_date'].dt.month.unique().tolist()
    month_list = sorted(month_list)
    # Checklist에 쓰일 goodsNo_list ==> 실제에서는 brand_list가 될 예정 
    goodsNo_list = doctorg['goodsNo'].unique().tolist()
    
    return year_list, month_list, goodsNo_list

# test형 월별로 나눈 데이터 프레임 생성
def make_new_test_df(df):
    
    new_df = df.groupby(['goodsNo', 'review_month'])['gdasCont'].count().unstack()
    new_df.columns = ['Jan', 'Feb', 'Mar', 'Apr']
    new_df = new_df[:10].copy()
    return new_df


doctorg_23 = bring_test_2023_data()
year_list, month_list, goodsNo_list = bring_needed_list(doctorg_23)
new_df = make_new_test_df(doctorg_23)
new_df.to_csv('test_app_csv.csv', index=True)

#시험해보기
    fig12, ax = plt.subplots(figsize=(12,8))
    x=np.arange(len(df.brand_name.unique()))
    bar_width = 0.4
    b1=ax.bar(x, df.loc[df['stars_updated'] == 6, 'count'],
              width=bar_width)
    b2=ax.bar(x +bar_width, df.loc[df['stars_updated'] == 5, 'count'],
              width=bar_width)
    ax.legend(title='Stars', loc='upper right')
    st.pyplot(fig12)
    
    #색깔로 별점 구분하기.
    fig11, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x="brand_name", y="stars_updated", hue="stars_updated", data=df, ax=ax)
    ax.set_title("Brand vs Stars Updated Count", fontsize=18)
    ax.set_xlabel("Brand", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    st.pyplot(fig11)
    
    
    grouped_data = df.groupby(['brand_name', 'stars_updated']).size().reset_index(name='count')
    # 막대 그래프 생성
    fig10, ax = plt.subplots(figsize=(12, 8))

    # x축에는 brand 칼럼 값을, y축에는 count 칼럼 값을 지정하여 막대 그래프 생성
    for stars_updated, color in zip(grouped_data['stars_updated'].unique(), ['red', 'orange', 'yellow', 'green', 'blue', 'purple']):
        filtered_data = grouped_data[grouped_data['stars_updated'] == stars_updated]
        ax.bar(filtered_data['brand_name'], filtered_data['count'], label=stars_updated, color=color)

    ax.legend(title='Stars', loc='upper right')

    st.pyplot(fig10)

    #산점도
    fig9 = px.scatter(df, x='brand_name', y='stars_updated', color='stars_updated', 
            title='Stars Updated by Brand', labels={'stars_updated': 'Stars'})
    st.plotly_chart(fig9)
    
    #리뷰분포도 bar 차트
    fig5=px.bar(df, x='stars_updated', y='brand_name')
    st.plotly_chart(fig5)
    
    #평균값 구해보기.
    df_grouped = df.groupby('brand_name').mean()
    fig7=px.bar(df_grouped, x=df_grouped.index, y='stars_updated',
               title='Stars Updated by Brand', labels={'stars_updated': 'Stars'})
    st.plotly_chart(fig7)
    
    
    st.subheader('브랜드별 리뷰 데이터 분포')
    df_sorted=df.sort_values('stars_updated',ascending=False)
    fig3=px.bar(df, x='brand_name', y='stars_updated')
    st.plotly_chart(fig3)
    
    
    
    #3. 파이차트 만들어보기.
    fig4 = px.pie(df['stars_updated'], title='Pie Chart of Languages')      #plotly pie차트
    st.plotly_chart(fig4)
    
    #
    
    #six_star_rating=df.loc[(df['stars_updated'] == option)]
    
    
    
    # 이건 넣을것!
    # 2022년과 2023년 리뷰 추출
    df2 = df2[df2['review_year'].isin([2022, 2023])]

    # brand_name 칼럼 값 추출
    brands = df2['brand_name'].unique()

    # 시각화
    st.title('2022-2023 년도 브랜드 리뷰')
    brand_selected = st.multiselect('브랜드 선택', brands)

    if brand_selected:
        # 선택한 브랜드의 데이터 추출
        brand_data = df2[df2['brand_name'].isin(brand_selected)]
        
        # review_month와 brand_name으로 그룹화하여 total_score 계산
        monthly_scores = brand_data.groupby(['review_month', 'brand_name'])['total_score'].mean().unstack()
        
        # 선 그래프 시각화
        st.line_chart(monthly_scores)
        
        # 막대 그래프 시각화
        fig, ax = plt.subplots()
        monthly_scores.plot(kind='bar', ax=ax)
        ax.set_xlabel('월')
        ax.set_ylabel('평균 total_score')
        ax.set_title('2022-2023 년도 월별 평균 total_score')
        st.pyplot(fig)
        
        
    # time data 2022.0-.11.0 오류    
    st.title('testtest')
    # Load data
    df2 = pd.read_csv("final_df.csv")

    # Create a new column with datetime values based on review year and month
    df2["review_date"] = pd.to_datetime(df2["review_year"].astype(str) + "-" + df2["review_month"].astype(str), format="%Y-%m")

    # Filter data by brand name, year, and month
    brands = st.multiselect("Select brand(s)", df2["brand_name"].unique())
    years = st.multiselect("Select year(s)", [2022, 2023])
    months = st.multiselect("Select month(s)", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    df_filtered = df2.loc[(df2["brand_name"].isin(brands)) &
                        (df2["review_year"].isin(years)) &
                        (df2["review_month"].isin(months))]

    # Create date range slider
    start_date = pd.to_datetime(df_filtered["review_date"].min())
    end_date = pd.to_datetime(df_filtered["review_date"].max())
    date_range = st.slider("Select date range", start_date, end_date, (start_date, end_date))

    df_filtered = df_filtered.loc[(df_filtered["review_date"] >= date_range[0]) &
                                (df_filtered["review_date"] <= date_range[1])]

    # Create bar chart
    chart_data = df_filtered.groupby(["brand_name", "review_date"])["total_score"].sum().reset_index()

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("yearmonth(review_date):O", axis=alt.Axis(title="Date")),
        y=alt.Y("total_score:Q", stack=None, axis=alt.Axis(title="Total Score")),
        color="brand_name:N"
    ).properties(
        width=800,
        height=500
    ).interactive()

    st.altair_chart(chart)
    
    
         # 시각화 (쓸것)
    st.subheader('2022-2023 년도 브랜드 리뷰')
    brand_selected = st.selectbox('브랜드 선택', brands)

    if brand_selected:
        # 선택한 브랜드의 데이터 추출
        brand_data = df1[df1['brand_name']==brand_selected]
        
        # review_month로 그룹화하여 total_score 계산
        monthly_scores = brand_data.groupby('review_month')['total_score'].mean()
        
        plt.rcParams['font.family'] = 'NanumGothic'
        # 선 그래프 시각화
        fig13, ax1 = plt.subplots()
        monthly_scores.plot(kind='line', ax=ax1)
        ax1.set_xlabel('월')
        ax1.set_ylabel('평균 total_score')
        ax1.set_title(f'{brand_selected} 브랜드 2022-2023 년도 월별 평균 total_score')
        st.pyplot(fig13)
                
        # 막대 그래프 시각화
        fig14, ax = plt.subplots()
        ax.bar(monthly_scores.index, monthly_scores.values)
        ax.set_xlabel('월', fontsize = 12)
        ax.set_ylabel('평균 total_score', fontsize = 12)
        ax.set_title(f'{brand_selected} 브랜드 2022-2023 년도 월별 평균 total_score')
        st.pyplot(fig14)
    #st.text('텍스트를 입력해주세요')
    #st.header("")
    
    
    
        brand_selected = st.selectbox('브랜드 선택', brands)

    if brand_selected:
        # 선택한 브랜드의 데이터 추출
        brand_data = df1[df1['brand_name']==brand_selected]
        
        # review_month로 그룹화하여 total_score 계산
        monthly_scores = brand_data.groupby('review_month')['total_score'].mean()
        
        plt.rcParams['font.family'] = 'NanumGothic'
        # 선 그래프 시각화
        fig13, ax1 = plt.subplots()
        monthly_scores.plot(kind='line', ax=ax1)
        ax1.set_xlabel('월')
        ax1.set_ylabel('평균 total_score')
        ax1.set_title(f'{brand_selected} 브랜드 2022-2023 년도 월별 평균 total_score')
        st.pyplot(fig13)
        
        # 막대 그래프 시각화
        fig14, ax = plt.subplots()
        ax.bar(monthly_scores.index, monthly_scores.values)
        ax.set_xlabel('월', fontsize = 12)
        ax.set_ylabel('평균 total_score', fontsize = 12)
        ax.set_title(f'{brand_selected} 브랜드 2022-2023 년도 월별 평균 total_score')
        st.pyplot(fig14)
        
        
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt