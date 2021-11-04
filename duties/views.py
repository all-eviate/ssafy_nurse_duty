from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
import statistics
import datetime
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



duties = set() # 근무표의 리스트를 중복제거를 위해 집합으로 선언
last_duty = ['O', 'D', 'E', 'N'] # 지난달 마지막 주 근무표를 받아와야 함
duty = ['P'] # 인덱스를 맞추기 위해 [P]adding을 붙여둠
sample = [10, 7, 7, 7] # 표준편차 계산을 위한 샘플 데이터셋 (수정 예정)
std = statistics.stdev(sample) # 표준편차 값
recovery = 0 # 이번 달 recovery off의 지급 여부
offs = [1, 13, 15, 26] # off 요청의 예시
holiday = [] # 주말 이외의 공휴일 데이터셋 // 이부분은 어떻게 API나 그런걸 쓰면서 받아와야 할 듯

def dfs(date, month, age, yoil): 
    global duty
    global recovery
    global missed_off
    global yom
    # 일단 길이가 다 찼다면
    if date > month:
        # 듀티 리스트에 해당 듀티를 추가
        print(summary)
        good = True
        for counts in summary.values():
            if counts < 5:
                good = False
                break
        if good:
            duties.add(''.join(duty[1:month + 1]))
        return

    if yoil == 5 or yoil == 6 or date in holiday: # 오늘이 휴일이면 누적 오프 증가
        missed_off += 1

    # 오프 받고 싶은 날
    if date in off_requests:
        NEXT = ['O']
    else:
        if duty[date-1] == 'D':
            if age > 40:
                NEXT = ['D', 'E', 'O']
                if missed_off > 0:
                    NEXT = ['O', 'D', 'E']
            else:
                # 듀티 규칙 [월-2항]
                if summary['N'] < 7 or (summary['N'] == 7 and not recovery):
                    NEXT = ['D', 'E', 'N', 'O']
                    if missed_off > 0:
                        NEXT = ['O', 'D', 'E', 'N']
                else:
                    NEXT = ['D', 'E', 'O']
                    if missed_off > 0:
                        NEXT = ['O', 'D', 'E']
        elif duty[date-1] == 'E':
            if age > 40:
                NEXT = ['E', 'O']
                if missed_off > 0:
                    NEXT = ['O', 'E']
            else:
                # 듀티 규칙 [월-2항]
                if summary['N'] < 7 or (summary['N'] == 7 and not recovery):
                    NEXT = ['E', 'N', 'O']
                    if missed_off > 0:
                        NEXT = ['O', 'E', 'N']
                else:
                    NEXT = ['E', 'O']
                    if missed_off > 0:
                        NEXT = ['O', 'E']
        elif duty[date-1] == 'N': # 이미 40세 이하
            NEXT = ['O']
        else: # 전날 오프
            # N-O-D 방지
            if duty[date-2] == 'N':
                NEXT = ['E', 'N', 'O']
                if missed_off > 0:
                    NEXT = ['O', 'E', 'N']
            else:
                if age > 40:
                    NEXT = ['D', 'E', 'O']
                    if missed_off > 0:
                        NEXT = ['O', 'D', 'E']
                else:
                    # 듀티 규칙 [월-2항]
                    if summary['N'] < 7 or (summary['N'] == 7 and not recovery):
                        NEXT = ['D', 'E', 'N', 'O']
                        if missed_off > 0:
                            NEXT = ['O', 'D', 'E', 'N']
                    else:
                        NEXT = ['D', 'E', 'O']
                        if missed_off > 0:
                            NEXT = ['O', 'D', 'E']
    for _ in NEXT:
        nextduty = random.sample(NEXT)
        if nextduty in ['D', 'E', 'N'] and summary[nextduty] == 7:
            continue
        if date >= 4 and nextduty == duty[date-1] == duty[date-2] == duty[date-3]:
            continue
        duty.append(nextduty) # += nextduty
        summary[nextduty] += 1
        if nextduty == 'N' and summary['N'] == 7 and not recovery:
            duty.append('O') # += 'O'
            summary['O'] += 1
            missed_off -= 1 # 오프를 받았다면 누적 오프 하나 해결
            recovery = 1
            dfs(date + 2, month, age, (yoil + 2) % 7)
            duty.pop() # -= 'O'
            summary['O'] -= 1
            missed_off += 1
            recovery = 0
        else:
            if nextduty == 'O':
                missed_off -= 1
            dfs(date + 1, month, age, (yoil + 1) % 7)
            if nextduty == 'O':
                missed_off += 1
        summary[nextduty] -= 1
        duty.pop() # -= nextduty


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
@login_required
def index(request):
    today = get_date(request.GET.get('month'))

    prev_month_var = prev_month(today)
    next_month_var = next_month(today)

    cal = Calendar(today.year, today.month)
    html_cal = cal.formatmonth(withyear=True, user=request.user)
    result_cal = mark_safe(html_cal)

    context = {'calendar' : result_cal, 'prev_month' : prev_month_var, 'next_month' : next_month_var}

    return render(request, 'duties/index.html', context)

def dutylist(request):
    return render(request, 'duties/dutylist.html')


#현재 달력을 보고 있는 시점의 시간을 반환
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

#현재 달력의 이전 달 URL 반환
def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

#현재 달력의 다음 달 URL 반환
def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#새로운 Event의 등록 (모든 유저에 등록이 발생)
def event(request, event_id=None):
    # duty 전체 정보, 원하는 달, 듀티표 로드
    team = get_object_or_404(Team, pk=1)
    month = request.POST.get('month')
    dutys = team.duty.get(month)

    # for문을 이용해 그 달에 넣기
    nurse_num = 1
    for user_pk in range(1, nurse_num+1): # 관계 연결이 아니다보니 이런 방식이여야함
        nurse = get_object_or_404(get_user_model(), pk=user_pk)
        user_duty = dutys[user_pk] # ['D', 'E', 'N', 'O', 'D', 'E', 'N', 'O', 'D', 'E', 'N', 'O', 'D', 'E', 'N', 'O', 'D', 'E', 'N', 'O', 'D', 'E', 'N', 'O', 'D', 'E', 'N', 'O', 'D', 'E']
        for idx in range(len(user_duty)):
            start_time = f"2021-{month}-{idx+1} 00:00:00"
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
            Event.objects.create(user=nurse, start_time=start_time, title=title)
    
    return redirect('duties:index')

