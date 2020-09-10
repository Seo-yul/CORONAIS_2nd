from django.urls import path
from . import views

urlpatterns = [
    # loacalhost:8000/ : 템플릿 적용한 메인 페이지
    path('', views.cois_main, name='cois-main'),

    # 전국 지도 페이지
    path('folium_page/', views.folium_page, name='folium'),

    # data 등록
    path('data-init/', views.call_data_init, name='data-init'),

]
