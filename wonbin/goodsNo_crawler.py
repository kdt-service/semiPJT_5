import pandas as pd
import numpy as np
import requests
import json
import time

skincare_dict = {
    '10000010001' : [ # 스킨케어
        '100000100010008', # 토너/로션/올인원
        '100000100010009', # 에센스/크림
        '100000100010010'# 미스트/오일
    ]
}


def bring_goodsNo():
    global skincare_dict
    brand_list = ['닥터지', '라운드랩', '라네즈', '아이소이', '아누아', '에스트라'] 
    brand_subcat_item_dict = { # 정보를 담아줄 dictionary ==> 나중에 json파일로 저장
        '닥터지' : {},
        '라운드랩' : {},
        '라네즈' : {},
        '아이소이' : {},
        '아누아' : {},
        '에스트라' : {}
    }
    for brand in brand_list:
        for main, subs in skincare_dict.items():
            for sub in subs:
                try: # category_dict에 있는 메인 혹은 서브 카테고리가 해당 브랜드에 없을 수도 있기 때문에
                     # 없는 경우 오류를 내지 않고 넘어가주도록 합니다. 
                    startCount = 0
                    while True:
                        base_url = 'https://www.oliveyoung.co.kr/store/search/NewMainSearchApi.do?'
                        params_01 = {
                            'query' : brand, # 브랜드별
                            'collection': 'OLIVE_GOODS,OLIVE_PLAN,OLIVE_EVENT,OLIVE_BRAND',
                            'listnum': '36',      
                            'startCount' : startCount, # listnum이 36이 넘어가는 경우 그 다음 페이지도 가져올 수 있도록
                            'sort' : 'RNK/DESC',
                            'goods_sort' : 'WEIGHT/DESC,RNK/DESC',
                            'disPlayCateId' : main,
                            'cateId': main, # main category
                            'cateId2': sub, # sub category
                            'typeChk' : 'thum',
                            'quickYn' : 'N'
                        }

                        headers = { 'X-Requested-With' : 'XMLHttpRequest'}
                        res = requests.get(base_url, headers = headers, params=params_01)
                        crawled_data = json.loads(res.json())

                        check_list = list() # 다음페이지의 상품 리스트가 있는지 없는지 확인하기 위한 리스트 
                        goodsNo_list = list()
                        for data in crawled_data['Data'][0]['Result']: # 'Result'=>'GOODS_NO'에 상품번호
                            check_list.append(data['GOODS_NO']) 
                        goodsNo_list = check_list # tiem
                        brand_subcat_item_dict[brand][sub] = goodsNo_list

                        startCount += int(params_01['listnum']) # startCount를 listnum만큼 넣어주고 다음 페이지로 이동합니다
                        if len(check_list) <= int(params_01['listnum']): # 다음 페이지에 listnum만큼 없는 경우 break를 하고 다음으로 이동
                            break
                except: # 메인 혹은 서브 카테고리가 없는 경우 넘어가주기 
                    continue

                    time.sleep(0.3) # 혹시나 블락을 당할 경우를 고려하여 time.sleep()을 줍니다.
          
    # json 파일로 저장해주기 
    file_path = "./goodsNo_dict.json"
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        json.dump(brand_subcat_item_dict, file, indent='\t')

    return 

if __name__ == '__main__':
    bring_goodsNo()

