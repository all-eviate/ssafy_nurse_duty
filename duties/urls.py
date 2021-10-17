from django.urls import path
from . import views

app_name = 'duties'
urlpatterns = [
    path('', views.index, name='index'),
    # path('selectmonth/', views.selectmonth, name='selectmonth'), 
    path('<int:pk>/', views.detail, name='detail'),
    path('dutylist/', views.dutylist, name='dutylist'),
    # path('pickoff/', views.pickoff, name='pickoff'), # OFF_request
    # path('pickoff/<int:month>/', views.pickoff, name='pickoff'),
]
