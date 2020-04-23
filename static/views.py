from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from user.models import Message
# Create your views here.

def about(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    context = {
        "count":count
    }
    
    return render(request, 'static/about.html', context)

def FAQ(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    context = {
        "count":count
    }
    return render(request, 'static/FAQ.html', context)