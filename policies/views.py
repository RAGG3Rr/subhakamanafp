from django.shortcuts import render
from .models import *

# Create your views here.
def policy(request):
    template = "policies/policies.html"

    policies = PrivacyPolicy.objects.all()

    context={
        'policies': policies,
    }

    return render(request, template, context)

def exchange(request):
  template = "policies/exchange.html"
    
  exchange = Exchange.objects.all()

  context={
      'obj': exchange,
    
  }
  return render(request, template,context)