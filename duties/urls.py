from django.urls import path
from . import views

app_name = 'duties'
urlpatterns = [
    path('', views.index, name='index'), # 달력
    path('new/', views.event, name="new"), # 달력 리뉴얼
    path('dutylist/', views.dutylist, name='dutylist'),
    path('edit/<int:event_id>', views.event, name="edit"),
    path('test/', views.test, name='test'),
]
