from django.urls import path
from . import views

app_name = 'duties'
urlpatterns = [
    path('', views.index, name='index'), # 메인 화면
    path('<int:pk>/', views.read, name='read'), # 근무표 조회
    path('<int:pk>/generate-duty/', views.generateDuty, name='generateDuty')
]
