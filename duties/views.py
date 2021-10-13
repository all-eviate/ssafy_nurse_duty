from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Nurse, Team
from .forms import NurseForm
import statistics
import datetime
import holidays

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
    for nextduty in NEXT:
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
페이지 관리
"""

@login_required
@require_safe
def index(request):
    # Team 정보를 불러온다
    now_year = datetime.date.today().year
    now_month = datetime.date.today().month
    start_day, closing_day = calendar_get(now_year, now_month)


    # index에 달력 만들도록 정보를 넘긴다
    content = {
        'start_day': start_day, # 1일의 요일
        'closing_day': closing_day, # 마지막 날짜
    }
    return render(request, 'duties/index.html', content)

@login_required
@require_http_methods(["GET", "POST"])
def select(request):
    if request.method == 'POST':
        form = NurseForm(request.POST)
        if form.is_valid(): # 추후 유효성 추가 (선착순 등)
            form.save()
            return redirect('duties:index')
    else:
        form = NurseForm()
    context = {
        'form': form,
    }
    return render(request, 'duties/select.html', context)

@login_required
@require_safe
def detail(request, pk):
    # 모델로부터 간호사의 근무 조건을 받습니다
    nurse = Nurse.objects.get(pk=pk)
    context = {
        'nurse': nurse,
    }
    return render(request, 'duties/detail.html', context)

def dutylist(request):
    return render(request, 'duties/dutylist.html')
