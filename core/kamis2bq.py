#GCP debain 환경에서 실행되는 코드

import pandas as pd
from web_api_kamis import *
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import time

# df_cd = pd.read_csv('./Data/category_detail_code.csv', encoding = 'euc-kr')
#데이터 불러오기 및 전처리
start = time.time()
df_str = kamis_api_2(itemcode ='226')
df_str = df_str.assign(date = lambda x : df_str['연도'] + '/' + df_str['날짜'])
df_str['date'] = pd.to_datetime(df_str['date'], format = 'ISO8601')
df_str = df_str.assign(price_100g = lambda x: x['가격'].str.replace(',','').str.replace('-','0').astype('int')/20)
df_str.columns = ['itemcode','kindcode','countrycode','market','year','origin_date','tot_price','date','price_100g']
print('1/4 데이터 전처리 완료')

#빅쿼리 연결 설정
project_id = 'challenge-a-418407'
client = bigquery.Client(project=project_id)
dataset_id = 'kamis'
table_id = 'str'
full_dataset_id = "{}.{}".format(client.project, dataset_id)
print('2/4 빅쿼리 연결 설정 완료')

#스키마 설정(빅쿼리에 올라갈 데이터 형태)
schema = [
    bigquery.SchemaField("itemcode", "STRING"),
    bigquery.SchemaField("kindcode", "STRING", mode="NULLABLE"),  # NULL 값을 허용
    bigquery.SchemaField("countrycode", "STRING"),
    bigquery.SchemaField("market", "STRING", mode="NULLABLE"),  # NULL 값을 허용
    bigquery.SchemaField("year", "STRING"),  # 연도가 숫자로만 구성되어 있더라도, 여기서는 문자열로 처리
    bigquery.SchemaField("origin_date", "STRING"),  # 날짜를 문자열로 처리할 수 있지만, DATE 타입을 사용하는 것이 더 적합할 수 있음
    bigquery.SchemaField("tot_price", "STRING"),       
    bigquery.SchemaField("date", "DATE"),  # datetime64[ns] 타입은 BigQuery의 DATE 타입으로 매핑
    bigquery.SchemaField("price_100g", "FLOAT64"),  # float64 타입은 BigQuery의 FLOAT64 타입으로 매핑
]
job_config = bigquery.LoadJobConfig(schema=schema) 

dataset_ref = client.dataset(dataset_id)
# 데이터셋이 없을 경우, 데이터셋 생성
try:
    client.get_dataset(dataset_ref)
    print("{} 데이터셋 이미 존재".format(full_dataset_id))
except NotFound:
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = "asia-northeast3"
    client.create_dataset(dataset)
    print("{} 데이터셋 생성".format(full_dataset_id))

print('3/4 dataset 생성체크 완료')

# 테이블 존재 여부 확인
table_ref = client.dataset(dataset_id).table(table_id)
try:
    client.get_table(table_ref)
    client.delete_table(table_ref)
    print("{} 테이블이 존재하여 삭제.".format(table_id))
except NotFound:
    print("{} 테이블이 없어 생성필요".format(table_id))

job = client.load_table_from_dataframe(df_str, table_ref, job_config = job_config)
job.result()
end = time.time()
print("4/4 작업완료, {}초 소요".format(round(end-start)))
