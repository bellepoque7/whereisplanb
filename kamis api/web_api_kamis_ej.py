# 14번: 지역별 품목별 도.소매가격정보

import web_api_kamis as wak
import cert_info
import pandas as pd
import requests
import numpy as np
import xml.etree.ElementTree as ET 

def kamis_api_14(p_productclscode='01', p_regday='2020-07-16', p_itemcategorycode='100', p_itemcode='111', p_kindcode='01',p_productrankcode='07',p_countycode='1101',p_convert_kg_yn='Y'):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=ItemInfo'
    params = {
        ('p_cert_key', cert_info.cert_key()), #인증Key
        ('p_cert_id', cert_info.cert_id()),   #요청자id
        ('p_productclscode', p_productclscode),
        ('p_regday', p_regday),
        ('p_itemcategorycode', p_itemcategorycode),
        ('p_itemcode', p_itemcode),
        ('p_kindcode', p_kindcode),
        ('p_productrankcode', p_productrankcode),
        ('p_countycode', p_countycode),
        ('p_convert_kg_yn', p_convert_kg_yn),
        ('p_returntype', 'xml') 
        }
    
    response = requests.get(url, params)
    root = ET.fromstring(response.text)

    row_dict = {
            'p_productclscode':[],
            'p_itemcategorycode':[],
            'p_itemcode':[],
            'p_kindcode':[],
            'p_productrankcode':[],
            'p_countycode':[],
            'p_convert_kg_yn':[],
            'countyname':[],
            'itemname':[],
            'kindname':[],
            'unit':[],
            'price':[],
            'weekprice':[],
            'monthprice':[],
            'yearprice':[]
        }

    cnt = 0
    for i in root.findall("./data/item"):
        cnt = cnt + 1
        for j in i:
            row_dict[j.tag].append(j.text) 

    text = root.find("./condition/item")
    for i in range(1,cnt+1):
        row_dict['p_productclscode'].append(text.find("p_productclscode").text)
        row_dict['p_itemcategorycode'].append(text.find("p_itemcategorycode").text)
        row_dict['p_itemcode'].append(text.find("p_itemcode").text)
        row_dict['p_kindcode'].append(text.find("p_kindcode").text)
        row_dict['p_productrankcode'].append(text.find("p_productrankcode").text)
        row_dict['p_countycode'].append(text.find("p_countycode").text)
        row_dict['p_convert_kg_yn'].append(text.find("p_convert_kg_yn").text)

    df = pd.DataFrame(row_dict)
    df.columns =  ['구분','부류코드','품목코드','품종코드','등급코드','시군구코드','kg단위환산','countryname','itemname','kindname','단위','조회일자 가격','일주일전 가격','1개월전 가격','1년전 가격']

    return df
 
