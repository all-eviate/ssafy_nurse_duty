from django.urls import path
from . import views

app_name = 'duties'
urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select, name='select'),
    path('<int:pk>/', views.detail, name='detail'),
]
