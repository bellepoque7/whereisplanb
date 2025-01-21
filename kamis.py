import requests
import pandas as pd
import os
import xml.etree.ElementTree as ET


def dailypricecategory(
    cls_code: str = '02',
    category_detail_code: str = '224',
    country_code: str = '',
    regday: str = '2022-12-01',
    convert_kg_yn: str = 'N',
) -> requests.Response:

    """
    API 1번("일별 부류별 도.소매가격정보")의 응답 상황을 확인하기 위한 함수입니다.
    """
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList'
    params = {
        'p_cert_key': os.environ['kamis_api_id'],
        'p_cert_id': os.environ['kamis_api_key'],
        'p_returntype': 'json',
        'p_product_cls_code': cls_code,
        'p_item_category_code': category_detail_code[0] + '00',
        'p_country_code': country_code,
        'p_regday': regday,
        'p_convert_kg_yn': convert_kg_yn
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, params=params, headers=headers)
    print(response.text[:100])
    return response



#https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=1
def xml2df():
    response = dailypricecategory()   
    root = ET.fromstring(response.text)
    
    row_dict = {'item_name':[],'item_code':[],'kind_name':[],'kind_code':[],'rank':[],'rank_code':[],
    'unit':[],'day1':[],'dpr1':[],'day2':[],'dpr2':[],'day3':[],'dpr3':[],'day4':[],'dpr4':[],'day5':[],'dpr5':[]
    ,'day6':[],'dpr6':[],'day7':[],'dpr7':[]}
    #data/item 계층 밑의 값을 list으로 가져와 iteration
    for i in root.findall('./data/item'):
        # item_name부터 텍스트를 가져와 딕셔너리에 저장
        for j in i:
            row_dict[j.tag].append(j.text)

    df = pd.DataFrame(row_dict)
    print(df.head(3))
    return df

def json2df():
    response = dailypricecategory()
    text = response.json()
    df = pd.json_normalize(text['data']['item'])
    print(df.head(3))
    return df

if __name__ == '__main__':
    print('''
          1. dailypricecategory: 일별 카테고리별 가겨
          2. xml2df: xml로 받아온 api를 df로 변환
          3. json2df: json로 받아온 api를 df로 변환
          ''')
    choice = input()
    
    if choice =='1':
        dailypricecategory()
    elif choice =='2':
        xml2df()
    elif choice =='3':
        json2df()
    
    