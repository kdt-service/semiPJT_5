from konlpy.tag import Mecab
from konlpy.tag import Kkma
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.max_columns = None

def from_reading_csv_to_making_final_df():
    """
    (감성 점수가 매겨진 컬럼들이 들어있는 데이터 프레임이 들어와야 합니다.)

    1. 데이터 프레임 import
    2. 날짜별로 나누어주기
    3. 1차적으로 감성 점수 폭 줄여주기
    4. 레이블링 ==> 감정 점수로 변환해주기
    5. 개별 점수화

    6. 브랜드별, 시간별, 리뷰별 그룹화 
    7. 스케일링 작업
    8. 
    """

    # 데이터 프레임 
#     df = pd.read_csv('/content/drive/MyDrive/oliveyoung_more_columns_with_scoring_KPIs.csv') # 코랩 경로
    df = pd.read_csv('./oliveyoung_more_columns_with_scoring_KPIs.csv')


    # 날짜 컬럼
    df['review_dates'] = pd.to_datetime(df['dispRegDate'])
    df['review_year'] = df['review_dates'].dt.year
    df['review_month'] = df['review_dates'].dt.month

    # 2023 데이터 + 2022년 11월, 12월 데이터 ==> 비교적 최근 데이터 가져오기
    df = df[((df['review_year'] == 2022) & (df['review_month'].isin([11,12]))) | (df['review_year'] == 2023)].copy()


    # +,-1로 된 점수들 점수 폭 줄여주기
    # why? ==> 감정 점수가 2,1,0,-1 인데 감성어 사전으로 +1,-1 이렇게 점수가 왔다갔다한다면
    # 원래 부정 감정을 가지고 있던 사람이 긍정으로 넘어갈 수 있는 경우가 있음.
    # 이러한 경우를 방지하기 위해 1차적으로 점수 변동 폭 줄여주기

    df['price/5'] =\
        df['price'] / 5
    df['formulation/5'] =\
        df['formulation'] / 5
    df['effects/5'] =\
        df['effects'] / 5
    df['components/5'] =\
        df['components'] / 5
    df['scent/5'] =\
        df['scent'] / 5

    # label to emotion_score 
    df.loc[(df['label'] == 3), 'emotion_score'] = 2
    df.loc[(df['label'] == 2), 'emotion_score'] = 1
    df.loc[(df['label'] == 1), 'emotion_score'] = 0
    df.loc[(df['label'] == 0), 'emotion_score'] = -1

    # 개별 점수화
    df['price_score'] =\
        df['price/5'] / (abs(df['price'] + df['formulation'] + df['effects'] + df['components'] + df['scent'])) 
    df['formul_score'] =\
        df['formulation/5'] / (abs(df['price'] + df['formulation'] + df['effects'] + df['components'] + df['scent'])) 
    df['effects_score'] =\
        df['effects/5'] / (abs(df['price'] + df['formulation'] + df['effects'] + df['components'] + df['scent'])) 
    df['compo_score'] =\
        df['components/5'] / (abs(df['price'] + df['formulation'] + df['effects'] + df['components'] + df['scent'])) 
    df['scent_score'] =\
        df['scent/5'] / (abs(df['price'] + df['formulation'] + df['effects'] + df['components'] + df['scent'])) 

    df['total_score'] =\
        df['emotion_score'] + df['price_score'] + df['formul_score'] + df['effects_score'] + df['compo_score'] + df['scent_score']

    # 결측치 채우기
    df.fillna(0, inplace=True)

    # 그룹화
    df_mean = df.groupby(['brand_name', 'review_year', 'review_month']).agg({'total_score' : 'mean',
                                                                         'gdasCont' : 'count'}).reset_index()
    df_mean.fillna(0, inplace=True) # 결측치 제거
    
    # 브랜드별, 날짜별 리뷰 수에 따른 데이터 스케일링
    for idx in range(len(df_mean)):
        df_mean.loc[idx, 'total_score_2'] = df_mean.loc[idx, 'total_score'] / (np.log1p(df_mean.loc[idx, 'gdasCont']))

    # 필요한 컬럼만 가져오고 컬럼 이름 변경 
    final_df = df_mean[['brand_name', 'review_year', 'review_month', 'total_score_2']]
    final_df = final_df.rename(columns = {'total_score_2' : 'total_score'})

    # csv 파일로 만들기 
#     final_df.to_csv('/content/drive/MyDrive/semiPJT_5_final_df.csv', index=False) # 코랩 경로
    final_df.to_csv('./semiPJT_5_final_df.csv', index=False)
    return final_df

if __name__ == "__main__":
    from_reading_csv_to_making_final_df()
    
    
    
    
    
    