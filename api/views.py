from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Member
import time
import json
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    time.sleep(6)
    content = "~~HELLO Fetch!!~~"
    # response = HttpResponse(content, "text/plain")
    response = HttpResponse(content, content_type="text/plain; charset=utf-8")
    return response

def travel(request):
    with open('static/scripts/travel.js', 'r', encoding='utf-8-sig') as f:
        content = f.read()
        json_str = content.replace("const spots =", "").strip().rstrip(';')

        data = json.loads(json_str)
        spots = data['CommonFormat'].get('Section', [])
        return JsonResponse(spots, safe=False)
    
def register(request):
# 取得 ?id=3的資料
    # name = request.GET.get("name","GUEST")
    # email = request.GET.get("email","guest@gmail.com")
    # age = request.GET.get("age",18)

# 接收 POST 傳過來FormData的資料
    name = request.POST.get("name","GUEST")
    email = request.POST.get("email","guest@gmail.com")
    age = request.POST.get("age",18)
    password = request.POST.get("password")
    password1 = request.POST.get("password1")
# 接收傳過來的檔案
    uploaded_file = request.FILES.get("avatar")

    file_name = None

# 把檔案寫進 uploads資料夾
    if uploaded_file:
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_file.name , uploaded_file)

    content = f"{name} 你好，你的電子郵件是{email}，今年{age}歲了，上傳{file_name}成功了!!"
    return HttpResponse(content, "text/plain; charset=utf-8")

def checkname(request):
    name = request.GET.get("name","GUEST")
    result = {
        "name_exists": False,
    }
    # 檢查用戶名是否存在
    if Member.objects.filter(user_name=name).exists():
        result["name_exists"] = True
    return JsonResponse(result, safe=False)

def checkemail(request):
    email = request.GET.get("email","guest@gmail.com")
    result = {
        "email_exists": False,
    }
    # 檢查電子郵箱是否存在
    if Member.objects.filter(user_email=email).exists():
        result["email_exists"] = True
    return JsonResponse(result, safe=False)

def checkpassword(request):
    password = request.GET.get("password")
    password1 = request.GET.get("password1")
    result = {
        "password_match": False,
    }
    # 檢查密碼是否相符
    if Member.objects.filter(user_password=password).exists():
        result["password_match"] = True
    return JsonResponse(result, safe=False)
