from django.shortcuts import render,redirect
from .models import *
from .forms import ApplyjobForm
from django.contrib import messages

# Create your views here.
def vacancy(request):
    template = "career/career.html"

    all_job=Job.objects.all()

    context={
        'all_job': all_job,
    }

    return render(request, template, context)

def vacancydetail(request,slug):
    specific=Job.objects.get(slug=slug)
    return render(request, "career/one_job.html", {'specific':specific})

def jobapply(request,slug):
    form = ApplyjobForm()
    job =Job.objects.get(slug= slug)

    if request.method == "POST":
        form = ApplyjobForm(request.POST or None, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.get_job = job
            form.save()
            messages.success(request, f'Successfully applied for the position.')
            return redirect('vacancy')

    context={
        "form" : form,
        "job": job
    }
    return render(request,'career/applyjob.html',context)    