from django.shortcuts import render
from .models import *

# Create your views here.
def faq(request):
    template = "faq/faq.html"

    faq = FAQ.objects.all()

    context={
        'faq': faq,
    }

    return render(request, template, context)