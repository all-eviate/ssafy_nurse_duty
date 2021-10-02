from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'), # 회원가입
    path('delete', views.delete, name='delete'), # 회원탈퇴
    path('login/', views.login, name='login'), # 로그인
    path('logout/', views.logout, name='logout'), # 로그아웃
    path('update/', views.update, name='update'), # 회원정보수정
]
