import requests
import pandas as pd
import os
import xml.etree.ElementTree as ET


def dailypricecategory(
    cls_code: str = '02',
    category_detail_code: str = '224',
    country_code: str = '',
    regday: str = '2022-12-01',
    convert_kg_yn: str = 'N'
) -> requests.Response:

    """
    API 1번("일별 부류별 도.소매가격정보")의 응답 상황을 확인하기 위한 함수입니다.
    
    category_detail_code: 고구마 품목코드는 151이며 100번을 호출한다음에 필터링해야함
    
    p_cert_key	string	인증Key
    p_cert_id	string	요청자id
    p_returntype	string	Return Type (json:Json 데이터 형식, xml:XML데이터형식)
    p_product_cls_code	string	구분 ( 01:소매, 02:도매, default:02 )
    p_item_category_code	string	부류코드(100:식량작물, 200:채소류, 300:특용작물, 400:과일류, 500:축산물, 600:수산물, default:100)
    p_country_code	string	* 소매가격 선택가능 지역 (1101:서울, 2100:부산, 2200:대구, 2300:인천, 2401:광주, 2501:대전, 2601:울산, 3111:수원, 3214:강릉, 3211:춘천, 3311:청주, 3511:전주, 3711:포항, 3911:제주, 3113:의정부, 3613:순천, 3714:안동, 3814:창원, 3145:용인, 2701:세종, 3112:성남, 3138:고양, 3411:천안, 3818:김해)<br />* 도매가격 선택가능 지역 (1101:서울, 2100:부산, 2200:대구, 2401:광주, 2501:대전)<br /> default : 전체지역
    p_regday	string	날짜 : yyyy-mm-dd (default : 최근 조사일자)
    p_convert_kg_yn	string	kg단위 환산여부(Y : 1kg 단위표시, N : 정보조사 단위표시, ex: 쌀 20kg)<br /> default : N
    """
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList'
    params = {
        'p_cert_key': os.environ['kamis_api_id'],
        'p_cert_id': os.environ['kamis_api_key'],
        'p_returntype': 'json',
        'p_product_cls_code': cls_code,
        'p_item_category_code': category_detail_code[0],
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
    
    