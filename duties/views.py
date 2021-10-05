from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Nurse
from .forms import NurseForm

# Create your views here.
def index(request):
    return render(request, 'duties/index.html')


def select(request):
    if request.method == 'POST':
        form = NurseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('duties:index')
    else:
        form = NurseForm()
    context = {
        'form': form,
    }
    return render(request, 'duties/select.html', context)


def detail(request, pk):
    nurse = Nurse.objects.get(pk=pk)
    context = {
        'nurse': nurse,
    }
    return render(request, 'duties/detail.html', context)
