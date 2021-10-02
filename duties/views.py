from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Nurse
from .forms import NurseForm

## 알고리즘
"""
알고리즘이 들어갈 부분입니다.
"""


## 페이지 관리
def index(request):
    return render(request, 'duties/index.html')

# 근무표 조회
def read(request, pk):
    pass
    # 알맞은 접근인지 인증합니다 (요청 확인)

    # 모델로부터 간호사의 근무 조건을 받습니다

    # 근무 조건을 html에 보냅니다


# 개인 근무표 생성 요청
def generateDuty(request, pk):
    # POST로 들어올때 (Form에서 받아옴)
    if request.method == "POST":
        pass
        # 들어온 정보의 유효성을 검사합니다. (선착순 기능)

        # DB에 저장합니다.

    # GET으로 들어올때
    else:
        pass
        # off_requests를 받는 Form을 html로 보냄