from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm, 
)
from .forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

# Create your views here.

# Create (회원가입)
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('duties:index') # 추후 맞춤(html)

    if request.method == "POST":
        form = UserCreationForm(request.POST) # 추후 맞춤(Model)
        if form.is_vaild():
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

# 회원정보 수정
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user) # 추후 맞춤(Model)
        if form.is_vaild():
            form.save()
            return redirect('duties:index')
    else:
        form = UserChangeForm(instance=request.user) # 추후 맞춤(Model)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
