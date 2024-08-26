from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Member
import time
import json
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from datetime import datetime

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
    content = "請完成填寫以便成功送出"
    # 接收 POST 傳過來FormData的資料
    if request.method == "POST":
        name = request.POST.get("name","GUEST")
        email = request.POST.get("email","guest@gmail.com")
        birth = request.POST.get("birth","2020-10-10")
        age = request.POST.get("age",18)
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        required_fields = [name, email, password, password1, birth]
        if any(not field for field in required_fields):
            error_message = "請填寫所有必填欄位：姓名、電子郵件、密碼、確認密碼和生日。"
            return HttpResponse(error_message, "text/plain; charset=utf-8")

        # 檢查用戶名是否存在
        if Member.objects.filter(user_name=name).exists():
            content = f"姓名： {name} 已被註冊，請重新輸入。"
            return HttpResponse(content, "text/plain; charset=utf-8")
        # 檢查電子郵件是否存在
        if Member.objects.filter(user_email=email).exists():
            content = f"電子郵件： {email} 已被註冊，請使用其他電子郵件。"
            return HttpResponse(content, "text/plain; charset=utf-8")
        # 檢查密碼是否一致
        if password != password1:
            content = f"密碼不一致，請重新確認。"
            return HttpResponse(content, "text/plain; charset=utf-8")

        # 接收傳過來的檔案
        uploaded_file = request.FILES.get("avatar")
        file_name = None

    # 把檔案寫進 uploads資料夾
        if uploaded_file:
            fs = FileSystemStorage()
            file_name = fs.save(uploaded_file.name , uploaded_file)


    # 將表單傳過來的資料寫進資料庫
        Member.objects.create(
            user_name = name,
            user_password = make_password(password),
            user_email = email,
            user_birth = birth,
            user_avator = file_name,
            last_update = datetime.now()
        )

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
    # 檢查電子郵件是否存在
    if Member.objects.filter(user_email=email).exists():
        result["email_exists"] = True
    return JsonResponse(result, safe=False)

def checkpassword(request):
    password = request.GET.get("password")
    result = {
        "password_match": False,
    }
    # 檢查密碼是否相符
    if Member.objects.filter(user_password=password).exists():
        result["password_match"] = True
    return JsonResponse(result, safe=False)
