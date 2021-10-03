from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.template import context, loader
from .models import User

from django.shortcuts import render, redirect

from django.contrib.auth.hashers import make_password, check_password #비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
# Create your views here.


class IndexView(TemplateView):
    
    template_name = 'index.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))


class CommunityView(TemplateView):
    
    template_name = 'community.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass

class CommunityVideoView(TemplateView):
    
    template_name = 'community_view.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass

class SignView(TemplateView):

    template_name = 'sign.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass

class ShareView(TemplateView):

    template_name = 'share.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass

class UserView(TemplateView):

    template_name = 'user_page.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass














def register(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        username = request.POST.get('username',None)   #딕셔너리형태
        password = request.POST.get('password',None)
        re_password = request.POST.get('re_password',None)
        res_data = {} 
        if not (username and password and re_password) :
            res_data['error'] = "모든 값을 입력해야 합니다."
        if password != re_password :
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error'] = '비밀번호가 다릅니다.'
        else :
            user = User(username=username, password=make_password(password))
            user.save()
        return render(request, 'register.html', res_data) #register를 요청받으면 register.html 로 응답.

def login(request):
    

    if request.method == "GET" :
        return render(request, 'login.html')

    elif request.method == "POST":
        login_username = request.POST.get('username', None)
        login_password = request.POST.get('password', None)

        response_data = {}
        if not (login_username and login_password):
            response_data['error']="아이디와 비밀번호를 모두 입력해주세요."
        else : 
            myuser = User.objects.get(username=login_username) 
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