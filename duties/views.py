from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Team
from accounts.models import User
# from .forms import NurseForm
from .schedule_maker import make_monthly_schedule, validate
import statistics
import datetime
from datetime import date
import holidays
from pprint import pprint

"""
알고리즘
"""
# 년, 월을 입력받아 공휴일정보 반환
def holyday_get(year, month):
    holidays_kr = holidays.KR()
    holyday_list = []
    for day in range(1, 32):
        check_day = str(month) + '/' + str(day) + '/' + str(year)
        try: # 31일까지 없는 달도 계산 수행 위함
            if check_day in holidays_kr:
                holyday_list.append(day)
        except:
            continue
    return holyday_list

# 년, 월을 입받아 시작요일, 마지막날짜 반환
def calendar_get(year, month):
    # 시작 요일 계산
    w = datetime.date(year, month, 1).weekday()

    # 마지막 날짜 계산
    m = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        m[2] = 29

    return (w, m[month]) # 리턴타입은 요일 숫자, 마지막 일
    # 0: 월요일 ~ 6: 일요일 (python 기본 방식이라고 함)


example_nurse_info = {
    1: [1, 0, 1, 0, 0, 0, 0, 0, 2, 0],
    2: [2, 1, 1, 0, 0, 0, 0, 0, 2, 0],
    3: [3, 2, 1, 0, 0, 0, 0, 0, 2, 0],
    4: [4, 0, 1, 0, 0, 0, 0, 0, 2, 0],
    5: [5, 1, 1, 0, 0, 0, 0, 0, 2, 0],
    6: [6, 2, 1, 0, 0, 0, 0, 0, 2, 0],
    # 7: [7, 0, 0, 0, 0, 0, 2, 0],
    # 8: [8, 0, 0, 0, 0, 0, 2, 0],
    # 9: [9, 0, 0, 0, 0, 0, 0, 0],
    # 10:[10, 0, 0, 0, 0, 0, 2, 0],
    # 11: [11, 0, 0, 0, 0, 0, 2, 0],
    # 12: [12, 0, 0, 0, 0, 0, 2, 0],
    # 13: [13, 0, 0, 0, 0, 0, 2, 0]
}

def test(request):
    valid = False
    while not valid:
        tdlist = []
        teamsduty = []
        for team in range(1, 3):
            nurses_list = User.objects.filter(emp_team = team)
            year_list = []
            # print(nurses_list)
            ni = {nurse.pk:[] for nurse in nurses_list}
            for nurse in nurses_list:
                year_list.append(nurse.emp_date)
                ni[nurse.pk] = [nurse.pk, nurse.emp_grade, nurse.emp_team, 0, 0, 0, 0, 0, 2, 0]
            sorted_year_list = sorted(year_list)
            middle_point = sorted_year_list[2]
            result, modified_nurse_info = make_monthly_schedule(
            team_list=[1],
            nurses_list=nurses_list,
            nurse_info=ni,
            needed_nurses_shift_by_team=1,
            # vacation_info=[],
            current_month=10,
            current_date=1,
            dates=31,
            start_day_of_this_month=0
            )
            ret = [[''] * 32 for nurse in nurses_list]
            # print('디버깅용 딕셔너리')
            # pprint(modified_nurse_info)
            # print()
            i = 1

            mapping = ['O', 'D', 'E', 'N']
            td = []
            for nurse in nurses_list:
                td.append(result[nurse.pk])
                for i in range(1, 32):
                    ret[nurse.pk % 6][i] = mapping[result[nurse.pk][i-1]]
                # print(nurse.emp_id, ret[nurse.emp_id])
            teamsduty.append(ret)
            tdlist.append(td)
        # print(tdlist)
        valid = validate(tdlist, 31, year_list, middle_point) # (년도, pk)

            # print(nurse.pk, result[nurse.pk])
    print(teamsduty)
    Team.objects.create(date=date.today(), duty={"1": teamsduty})
    
    return render(request, 'duties/index.html')


"""
회의 전까지 임시로 빼두겠습니다. 
뺐을때 장점: 기능별로 좀더 세분화 가능하다. 가독성이 좋다.(불확실)
            알고리즘 담당자가 try-error 하기 편하다.
       단점: 지저분하고 한번에 코드 기능을 알기 어려울 수 있다. 
"""
# select 함수(off_request 받아옴)뒤에서 사용
# 사용자의 pk를 받음. DB Nurse/duties에 dfs 결과 저장 
def off_request_save(pk):
    # off_request 불러오기
    now_month = str(datetime.date.today().month) + '월'
    nurse = Nurse.objects.get(pk=pk)
    nurse_choice = nurse.choices.get(now_month)

    off_request = []
    for day, flag in nurse_choice.items():
        if flag: # True값이면
            off_request.append(day)

    # 알고리즘 수행
    # result_duty_raw = function_dfs(off_request, ~~, ~~)
    result_duty_raw = ['112134231243', # 나중에 위에 주석과 교환
                       '112134231244',
                       '112134231245',]
    
    if nurse.duties == None: # 초기에 비어있으면
        nurse_duties = {now_month: result_duty_raw} # 저장
        nurse.save()
    else: # 일반적인 경우
        nurse_duties[now_month] = result_duty_raw
        nurse.save()
    return 

"""
페이지 관리
"""

def index(request):

    return render(request, 'duties/index.html')

def dutylist(request):
    return render(request, 'duties/dutylist.html')