from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),  # 회원 가입
    path('delete/', views.delete, name='delete'),  # 회원 탈퇴
    path('update/', views.update, name='update'),  # 회원정보 수정
    path('password/', views.change_password, name='change_password'),  # 비밀번호 수정
    path('login/', views.login, name='login'),  # 로그인
    path('logout/', views.logout, name='logout'),  # 로그아웃
    path('<int:pk>/', views.profile, name='profile'),  # 프로필
]