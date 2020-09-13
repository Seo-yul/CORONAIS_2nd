from corona_map.Api import Gugun_status
from corona_map.Api import Gugun_status_calc

from corona_map.Api import Infection_city, Infection_status, Infection_by_age_gender, News_board
from bs4 import BeautifulSoup
import requests
"""
    Title: data_init.py
    Detail: database init function module
    Last-Modified: 20-09-05
    Author:	윤서율
    Created: 20-08-27
"""

def seoul_data_init():
    flag = Gugun_status.init_gugun_data()           # 서울 데이터 크롤링 및 데이터 생성

    if flag:
        Gugun_status_calc.init_seoul_calc_data()    # 서울 구 가공 데이터 생성


def folium_data_init():
    # 지도 데이터 초기화
    # mongodb collection infection_city에 api request해서 데이터 저장.
    Infection_city.infection_city()                         # 광역/특별시, 도 현황 데이터
    News_board.news_board_list()                            # 기사 데이터
    Infection_by_age_gender.infection_by_age_gender()       # 연령별 데이터
    Infection_status.infection_status()                     # 전국 현황 데이터

