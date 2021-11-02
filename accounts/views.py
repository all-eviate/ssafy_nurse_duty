from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm, 
    PasswordChangeForm,
)
from .forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.

# Create (회원가입)
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('duties:index') # 추후 맞춤(html)

    if request.method == "POST":
        form = UserCreationForm(request.POST, request.FILES) # 추후 맞춤(Model)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('duties:index') # 추후 맞춤(html)
    else:
        form = UserCreationForm() # 추후 맞춤(Model)
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# Delete (회원탈퇴)
@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete() 
        auth_logout(request) 
    return redirect('duties:index')

# Login (로그인)
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('duties:index') # 추후 맞춤(html)

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'duties:index') # 추후 맞춤(html)
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

# Logout (로그아웃)
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('duties:index') # 추후 맞춤(html)

# 프로필
@login_required
def profile(request, emp_id):
    user = User.objects.get(emp_id=emp_id)
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)

# 회원정보 수정
# @login_required
# @require_http_methods(['GET', 'POST'])
# def update(request):
#     if request.method == "POST":
#         form = UserChangeForm(request.POST, instance=request.user) # 추후 맞춤(Model)
#         if form.is_valid():
#             form.save()
#             return redirect('duties:index')
#     else:
#         form = UserChangeForm(instance=request.user) # 추후 맞춤(Model)
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/update.html', context)

# 비밀정보 수정
@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('duties:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

# 회원정보 수정 페이지랑 비밀번호 수정 페이지 합친것
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == "POST":
        form1 = UserChangeForm(request.POST, instance=request.user) # 추후 맞춤(Model)
        form2 = PasswordChangeForm(request.user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('duties:index')
    else:
        form1 = UserChangeForm(instance=request.user) # 추후 맞춤(Model)
        form2 = PasswordChangeForm(request.user)
    context = {
        'form1': form1,
        'form2' : form2,
    }
    return render(request, 'accounts/update.html', context)