from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Nurse
from .forms import NurseForm

# Create your views here.
def index(request):
    return render(request, 'duties/index.html')
