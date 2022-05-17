# CORONAIS_2nd

CORONAIS_2nd 는 팀 프로젝트가 끝난 후 클라우드 DB와 배포 및 추가 기능을 위해 CORONAIS를 포크한 개인 리모트 입니다.

이전 프로젝트에서는 공공데이터에서 제공하지 않는 상세 데이터를 가공하여 시각화 하였습니다.  

2nd 버전은 해당 외부에서 요청시 상세 데이터를 제공하는 **API 서비스**와 해당 API를 이용한 **정보제공 챗봇**, 실제 웹 사이트의 **배포**를 목적으로 진행됩니다.



---------

> CORONAIS
>
>  공공데이터 API에서 제공하는 코로나-19 데이터는 각 시도/시 등 큰 행정구역별 데이터만 제공하고 있으며, 각 자치단체 홈페이지 또한 확진자를 제외한 자세한 내용은 종합하여 제공하고 있지 않았습니다. 때문에 작은 행정단위 구역의 정보또한 종합하여 제공하여 비교할 수 있는 데이터를 알기 쉽게 제공하고자 해당 웹 사이트를 제작하게 되었습니다.



# 프로젝트 정보
## 프로젝트 기간
2020.08.10 ~ 2020.09.04  forked -> 2020.09.05 ~ 2020.10.31 서비스 종료

## 인원
3인 -> 1인

## 개발 플랫폼
Windows 10, CentOS
## 개발 툴
pycharm, robomongo
## 사용 언어
Python 3.7.8
## 사용 기술
Django, MongoDB, ngninx
# 데이터베이스 구조 (MongoDB)
![ERD](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/ERD.png)
# 스토리보드
![스토리보드-1](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/스토리보드1.jpg)
![스토리보드-1](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/스토리보드2.jpg)
# 제공 서비스
## 전국 코로나 현황

공공데이터 포털 API의 데이터를 시각화 할 뿐만 아니라 데이터를 가공하여 전국 일일 확진자 변화 양상과 지역별 일일 확진자 추이 정보를 보여준다.

또한, 지도의 마커를 클릭하여 지역별 데이터를 확인하거나 페이지를 이동하여 상세 데이터를 확인 할 수 있다.

![메인페이지-1](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/mainpage-1.PNG)
![메인페이지-2](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/mainpage-2.PNG)

## 상세 코로나 현황

공공데이터 포털의 API 에서 제공하지 않는 상세 데이터를 제공하는 페이지. 

각 시/도/구의 홈페이지에서 크롤링을 통해 직접 데이터를 가져와 제공한다.

![서울시 코로나 현황-1](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/detail-seoul-1.PNG)
![서울시 코로나 현황-2](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/detail-seoul-2.PNG)
## 뉴스

코로나 키워드로 뉴스를 검색하여 해당하는 기사를 최근순으로 보여준다.

![뉴스 게시글 목록-1](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/corona-new-1.PNG)
![뉴스 게시글-1](https://raw.githubusercontent.com/hackzoomuck/CORONAIS/master/coronais-photo/corona-new-detail-1.PNG)
# 환경 설정
## 가상 환경 설정 (venv)
새로운 venv 환경설정시, <br>
pip install git+https://github.com/python-visualization/branca.git@master <br>
명령을 내린 후 pip install 해야함.
(folium encoding 관련)
```
ERROR: Could not find a version that satisfies the requirement branca==0.4.1+3.g5887b9b (from -r requirements.txt (line 3)) (from versions: 0.1.1, 0.2.0, 0.3.0, 0.3.1, 0.4.0, 0.4.1)
ERROR: No matching distribution found for branca==0.4.1+3.g5887b9b (from -r requirements.txt (line 3))
```
하지 않을 경우 위와 같은 에러를 만날 수 있음.
## 데이터 베이스 설정
1. CORONAIS/settings.py 에서 DATABASES: 'HOST'에 DB서버의 IP를 기입 (약 80번째 줄 시작)
```python
'default': {
        'ENGINE': 'djongo',
        'NAME': 'coronais', # DB명
        'USER': 'coronais', # 데이터베이스 계정
        'PASSWORD':'coronais', # 계정 비밀번호
        'HOST':'localhost', # 데이테베이스 IP
        'PORT':'27017', # 데이터베이스 port
     }
```
2. 몽고디비에 기본 컬렉션을 만들어준다. (RDB의 테이블)
터미널에서 파이썬 마이그레이션 명령 실행
```bash
python manage.py makemigrations
python manage.py migrate
```
3.  corona_map/MongoDbManage.py 에서 연결 IP도 수정해준다.
현재 7 Line
```python
client = pymongo.MongoClient(host='localhost', port=27017)
```

# 남은 작업
1. 전국 시, 군, 구 별 현황.
데이터가 너무 많아 아직 서울시만 제공..
2. 각 데이터를 API로 제공.
3. 2.번의 API를 이용한 챗봇 기능 
