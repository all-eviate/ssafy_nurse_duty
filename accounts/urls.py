from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('signup/', views.signup, name='signup'), # 회원가입
    # path('delete', views.delete, name='delete'), # 회원탈퇴
    # path('login/', views.login, name='login'), # 로그인
    # path('logout/', views.logout, name='logout'), # 로그아웃
    # path('update/', views.update, name='update'), # 회원정보수정
    # # path('<int:pk>', views.profile, name='profile'), # 프로필 보여주기
    # path('change_password/', views.change_password, name='change_password'),  # 비밀번호수정
]