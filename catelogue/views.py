from catelogue.models import Catelogue
from django.shortcuts import render

def catelogue(request):
  context = {
    'catelogue': Catelogue.objects.all()
  }
  return render(request, 'catelogue/catelogue.html',context)