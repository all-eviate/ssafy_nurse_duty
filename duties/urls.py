from django.urls import path
from . import views

app_name = 'duties'
urlpatterns = [
    path('', views.index, name='index'), # 달력
    path('dutylist/', views.dutylist, name='dutylist'),
]
