from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import context, loader
from django.contrib.auth.hashers import make_password, check_password #비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)

from main.firebase_model import User
from server.settings import DB, BASE_DIR, PROJECT_DIR

class ErrorView(TemplateView):
    template_name = 'error.html'

    def get(self, req):
        return render(req, self.template_name)

class TestView(TemplateView):
    template_name = 'test.html'

    def get(self, req):
      
        pid = 'PSMHCkITg6zRxOJhnlwH'
        play_doc = DB.collection(u'Play').document(u'{}'.format(pid)).get()
        play_doc1 = DB.collection(u'Play').document(pid).get()
        play_doc2 = DB.collection(u'Play').document(u'PSMHCkITg6zRxOJhnlwH').get()
        print(play_doc.to_dict())
        print(play_doc1.to_dict())
        print(play_doc2.to_dict())


        # render(req,self.template_name, {"day":day,"id":id,"projectname":projectname })
        return render(req, self.template_name)


class IndexView(TemplateView):
    
    template_name = 'index.html'
    def get(self, req):

        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))


class CommunityView(TemplateView):
    
    template_name = 'community.html'
    def get(self, req):
        
        play_docs = DB.collection('Play').stream()
        data = []
        for doc in play_docs:
            play = doc.to_dict()
            date = play['date']
            play['date']  = '%04d-%02d-%02d %02d:%02d:%02d' % (date.year, date.month, date.day, date.hour+9, date.minute, date.second)
            data.append({'id' : doc.id, **play })
        
        print(data)
        context = {
            'plays' : data,
        }
        
        return render(req, self.template_name, context)


    def post(self, req):
        pass

class CommunityVideoView(TemplateView):
    
    template_name = 'community_view.html'

    def get(self, req, play_id):
        
        play_ref = DB.collection('Play').document(play_id)
        play_data = play_ref.get().to_dict()

        user_data = play_data['user'].get().to_dict()

        return render(req, self.template_name, {**play_data, 'user_name' : user_data['name']})

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

class RankingView(TemplateView):
    
    template_name = 'ranking.html'
    def get(self, req):
        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass

# Create your views here.
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
        elif password != re_password :
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error'] = '비밀번호가 다릅니다.'
        elif password == re_password : 
            res_data['error'] = None
            user = User(username=username, password=make_password(password))
            user.save()

        
        if res_data['error'] == None:
            return redirect('/user/login')         
        else:
            return render(request, 'register.html', res_data)  

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
            result = User.isExists(login_username)            
            if result:
                user = result.to_dict()
                if check_password(login_password, user['password']):
                    request.session['user'] = result.id

                    return redirect('/')
                else:
                    response_data['error'] = "비밀번호를 틀렸습니다."
            else:
                response_data['error'] = "존재하지 않는 이름입니다."

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