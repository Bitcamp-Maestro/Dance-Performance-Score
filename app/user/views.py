from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password #비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from django.views import View
from .models import User
from validate_email import validate_email

import json


class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body) # 데이터를 먼저 불러옴
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400) #// 400 Bad request
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry email in use, choose another one.'}, status=409) # resource is confliting with the one already have
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body) # 데이터를 먼저 불러옴
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric number'}, status=400) #// 400 Bad request
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry username in use, choose another one.'}, status=409) # resource is confliting with the one already have
        return JsonResponse({'username_valid': True})

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        # GET USER DATA 
        # VALIDATE 
        # create a user account

        username = request.POST.get('username',None)
        email = request.POST.get('email', None)
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                user = User(username=username, email=email, password=make_password(password))
                user.save()
                
                return redirect('/user/login')

        return render(request, 'register.html')


def login(request):
    

    if request.method == "GET" :
        return render(request, 'login.html')

    elif request.method == "POST":
        login_username = request.POST.get('email', None)
        login_password = request.POST.get('password', None)

        response_data = {}
        if not (login_username and login_password):
            response_data['error']="이메일과 비밀번호를 모두 입력해주세요."
        else : 
            myuser = User.objects.get(email=login_username) 
            #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            if check_password(login_password, myuser.password):
                request.session['user'] = myuser.id 
                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'login.html',response_data)

def home(request):
    user_id = request.session.get('user')
    if user_id :
        myuser_info = User.objects.get(pk=user_id)  #pk : primary key
        return HttpResponse(myuser_info.username)   # 로그인을 했다면, username 출력

    return HttpResponse('로그인을 해주세요.') #session에 user가 없다면, (로그인을 안했다면)
    
    
def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')