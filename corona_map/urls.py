from django.urls import path
from . import views


urlpatterns = [
    # loacalhost:8080/
    path('', views.coIs_home, name='coIs_home')
]