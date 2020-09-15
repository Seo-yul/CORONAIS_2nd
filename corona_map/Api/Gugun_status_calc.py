import datetime

from corona_map.Api import Gugun_status
import corona_map.MongoDbManager as DBmanager

"""
    Title: Gugun_status_calc.py
    Detail: DB에서 구 데이터를 가져와서 오늘 확진자, 오늘 완치자를 구하여 저장
    Last-Modified: 20-09-05
    Author:	윤서율
    Created: 20-08-31
"""

def get_seoul_calc_data_dict() -> dict():
    """
     get_seoul_calc_data_dict 오늘 확진자, 오늘 완치자를 구하는 함수 즉, 가공 데이터
     seoul_calc_data_dict 크롤링을 위한 데이터 파라미터
     return seoul_calc_data_dict 계산된 서울 dict형 데이터
    """

    seoul_gu_data_list = Gugun_status.get_seoul_data_list()                         # 오늘 서울의 구 데이터 생성
    seoul_gu_yesterday_data_list = Gugun_status.get_seoul_yesterday_data_list()     # 어제 서울의 구 데이터 조회

    seoul_gu_calc_data_list = list()
    print('오늘데이터')
    for new, old in zip(seoul_gu_data_list, seoul_gu_yesterday_data_list):      # 오늘의 데이터 생성

        print(new)
        seoul_gu_calc_data_dict = dict()
        seoul_gu_calc_data_dict['gubunsmall'] = new['gubunsmall']            # 구/군명(한글)
        seoul_gu_calc_data_dict['defcnt'] = int(new['defcnt'])               # 확진자 수(총확진자 현재감염중 + 총 완치수 + 사망자 수)
        seoul_gu_calc_data_dict['isolingcnt'] = int(new['isolingcnt'])       # 격리중 환자수(현재확진자수 감염중)

        seoul_gu_calc_data_dict['isolclearcnt'] = int(new['isolclearcnt'])   # 격리 해제 수(총 완치자)
        seoul_gu_calc_data_dict['deathcnt'] = int(new['deathcnt'])           # 사망자 수

        seoul_gu_calc_data_dict['incdec'] = int(new['defcnt']) - int(old['defcnt'])               # 전일대비 증감 수(오늘 확진자수)
        seoul_gu_calc_data_dict['curedcnt'] = int(new['isolclearcnt']) - int(old['isolclearcnt']) # 완치자 수(오늘 완치자수)

        seoul_gu_calc_data_list.append(seoul_gu_calc_data_dict)

    seoul_calc_data_dict = {
        'seoul': seoul_gu_calc_data_list,
        'stdday': int(datetime.datetime.now().strftime('%Y%m%d'))
    }

    return seoul_calc_data_dict


def init_seoul_calc_data():
    """
    init_seoul_calc_data 서울 데이터 초기화, DB에 저장.
    """
    seoul_data_dict = get_seoul_calc_data_dict()
    DBmanager.Infection_Smallcity_Calc().add_gugun_status_datas_on_collection(seoul_data_dict)


def get_seoul_calc_data_list() -> list:
    """
    get_seoul_calc_data_list 계산된 서울 상세 데이터를 조회
    seoul_gus_data_list 현재 시간이 14시 전이라면 어제의 데이터 이후라면 오늘의 데이터를 리턴
    """
    based_hour = int(datetime.datetime.now().strftime('%H'))
    if based_hour >= 14:
        now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
    else:
        timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
        now_date = int(timestamp.strftime('%Y%m%d'))

    sql_query_0 = {'stdday': now_date}
    sql_query_1 = {'_id': 0}

    cursor_obj = DBmanager.Infection_Smallcity_Calc().get_gugun_status_datas_from_collection(sql_query_0, sql_query_1)

    cursor_objs_list = list(cursor_obj)
    seoul_gus_data_list = list()

    for obj_dict in cursor_objs_list:
        if obj_dict.get('seoul'):
            seoul_gus_data_list = obj_dict['seoul']
            break

    return list(seoul_gus_data_list)    

def get_seoul_total_data_dict() -> dict:
    """
    get_seoul_total_data_dict : 서울 상세페이지 지도의 데이터를 조회
    seoul_total_dict : 지도 데이터 포맷의 key 맞춘 dict 형 데이터
    Author : 이지은
    """
    seoul_total = get_seoul_calc_data_list()
    seoul_total_dict = {'defcnt':0,'isolingcnt':0,'isolclearcnt':0,'deathcnt':0}
    for seoul_gugun in seoul_total:
        seoul_total_dict['defcnt'] += seoul_gugun['defcnt']
        if seoul_gugun['gubunsmall'] == '강남구':
            continue
        seoul_total_dict['isolingcnt'] += seoul_gugun['isolingcnt']
        seoul_total_dict['isolclearcnt'] += seoul_gugun['isolclearcnt']
        seoul_total_dict['deathcnt'] += seoul_gugun['deathcnt']

    return seoul_total_dict
  
def get_seoul_calc_all_data_list() -> list:
    """
    get_seoul_calc_all_data_list : 계산된 서울의 모든 상세 데이터 조회
    return list(cursor_obj) : 조회한 obj의 list형
    """
    cursor_obj = DBmanager.Infection_Smallcity_Calc().get_gugun_status_all_data_from_collection()
    return list(cursor_obj)

def get_daily_incdec_list() -> list:
    """
    get_daily_incdec_list : 서울 상세 데이터의 일일 증감량을 보여주기 위한 함수
    return seoul_daily_data_list : 일별 서울 상세 데이터 증감
    """
    seoul_all_data_list = get_seoul_calc_all_data_list()
    seoul_daily_data_list = list()
    for gu_data in seoul_all_data_list:
        seoul_daily_data_dict = dict()
        seoul_daily_data_dict['stdday'] = gu_data['stdday']
        seoul_daily_data_dict['incdec'] = 0

        for gu_dict in gu_data['seoul']:
            seoul_daily_data_dict['incdec'] += gu_dict['incdec']

        seoul_daily_data_list.append(seoul_daily_data_dict)

    return seoul_daily_data_list
