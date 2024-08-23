from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home/index.html', {"title": "Ajax Homework"})

def travel(request):
    return render(request, 'home/travel.html', {"title": "旅遊景點"})

def register(request):
    return render(request, 'home/register.html', {"title": "會員註冊"})