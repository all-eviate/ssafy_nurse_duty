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
import random
import calendar
from .calendar import Calendar
from django.utils.safestring import mark_safe
from .models import Team, Event
from django.contrib.auth import get_user_model

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
#### 추가 기능 (off_request) ####

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
"""
페이지 관리
"""
# 메인 페이지
@login_required
def index(request):
    today = get_date(request.GET.get('month'))

    prev_month_var = prev_month(today)
    next_month_var = next_month(today)

    cal = Calendar(today.year, today.month)
    html_cal = cal.formatmonth(withyear=True, user=request.user) # 로그인 간호사 듀티표 출력
    result_cal = mark_safe(html_cal)

    context = {'calendar' : result_cal, 'prev_month' : prev_month_var, 'next_month' : next_month_var}

    return render(request, 'duties/index.html', context)

# 달력 출력 함수
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

# 달력 출력 함수
def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

# 달력 출력 함수
def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# Calendar 모델 관리
@require_POST
def event(request, event_id=None):
    # duty 정보, 해당 달 로드
    month = request.POST.get('month')
    team = Team.objects.filter(date__month=month).last() # 입력 달의 가장 최신 객체
    dutys = team.duty.get('1') # key의 경우 1로 약속

    # 모델 입력
    nurse_num = get_user_model().objects.all().count()
    print(nurse_num)
    for user_pk in range(1, nurse_num+1): 
        nurse = get_object_or_404(get_user_model(), pk=user_pk)
        user_duty = dutys[user_pk]
        for idx in range(1, len(user_duty)+1): # ['','D','O','E',...]
            start_time = f"2021-{month}-{idx+1}"
            if user_duty[idx] == 'D':
                title = 'Day'
            elif user_duty[idx] == 'E':
                title = 'Evening'
            elif user_duty[idx] == 'N':
                title = 'Night'
            elif user_duty[idx] == 'O':
                title = 'Off'
            else:
                title = 'No data'
            try: # 그 달의 일수보다 많은 일수가 들어가는 경우 pass
                Event.objects.create(user=nurse, start_time=start_time, title=title)
            except:
                continue
    return redirect('duties:index')


# 추가 기능(off_request)
def dutylist(request):
    return render(request, 'duties/dutylist.html')
