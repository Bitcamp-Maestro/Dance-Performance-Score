from django import template
from django.views.generic.base import RedirectView
from play.models import OptionForm, Option, Play
from json.encoder import JSONEncoder
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.template import context, loader
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import socket
import json
# Create your views here.

class OptionView(TemplateView, RedirectView):
    template_name = 'option.html'

    def get(self, req, *args, **kwargs):

        # print(req)
        # template = loader.get_template(self.template_name)
        # context = {'test':1}
        # return HttpResponse(template.render(context, req))
    
        if req.session.get('user'):
            print(req)
            template = loader.get_template(self.template_name)
            context = {'test':1}
            return HttpResponse(template.render(context, req))
        else:
            return redirect('/user/login')
    def post(self, req, *args,**kwargs):
        print('option recived')
        print(req.POST)
        print(req.FILES)

        if req.POST['upload'] == 'upload':
            play_option = Option(mode = req.POST['mode'], upload=req.POST['upload'], songs=req.POST['songs'], video=req.FILES['video'])
            play_option.save()
        else :
            play_option = Option(mode = req.POST['mode'], upload=req.POST['upload'], songs=req.POST['songs'], video=req.FILES)
            play_option.save()
            
        # form = OptionForm(req.POST)
        # if form.is_valid() :
        #     form.save()
        pid = 'qwre1234'
        # return JsonResponse({
        #     'result': 200,
        #     }, json_dumps_params={'ensure_ascii': True})
        # return redirect('play')

        # post 받고 play 설정정보 response로 넘겨주기
        # response로 redirect가 안돼서 client에서 처리 
        res = HttpResponse(status=307)
        res['Location'] = f'/play/?pid={pid}'
        return res
        


class PlayView(TemplateView):
    template_name = 'play.html'
    
    def get(self, req, *args, **kwargs):
        # request에서 play 정보 parameter 정보 꼭 받기
        # 안받으면 main 이나 option 으로 render 하기(혹은 error 처리페이지로)
        
        print('play')
        print(req.GET)
        
        # print(req.GET.get('pid', None))
        # print(req.GET['pid'])
        user_option = Option.objects.last()
        print(user_option.video.url)
        host = "192.168.0.12"  # 챗봇 엔진 서버 IP 주소
        port = 5050  # 챗봇 엔진 서버 통신 포트
        mySocket = socket.socket()
        mySocket.connect((host, port))
        json_data = {
            "pid" : req.GET['pid'],
            "target" : "C:/JGBH/Dancer-Flow/model_server/module/sample_data/BTS-Dynamite1-3.mp4",
            "path" : "C:/JGBH/Dancer-Flow/model_server/module/sample_data/sample.mp4"
        }
        message = json.dumps(json_data)
        mySocket.send(message.encode())
        context = {
            'pid' : req.GET['pid'],
            'title' : 'Dynamite',
            'artist' : 'BTS',
            # 'play_mode' : 'upload',
            'play_mode' : user_option.upload,
            # 'video_url' : '/static/target_videos/dynamite.mp4',
            # 'video_url' : 'https://cache.midibus.kinxcdn.com/name/ch_17bdc199/17c131b8dd5313bf_720P',
            'video_url' : 'https://cache.midibus.kinxcdn.com/name/ch_17bdc199/17c5d6a3a8a8d84c_720P',
            # 'user_video_url' : 'http://192.168.0.12:5050/module/sample_data/result_test.mp4',
            'user_video_url' : user_option.video.url,
        }
        # return HttpResponse(template.render(context, req))
        return render(req, self.template_name, context)

    def post(self, req, *args, **kwargs):
        print(req)
        print('video reci`ved')
        print(req.POST)
        print(req.FILES)

        play_data = Play(datetime = req.POST['datetime'], score=int(req.POST['score']), video=req.FILES['video'])
        play_data.save()
        return JsonResponse({
            'result': 200,
        }, json_dumps_params={'ensure_ascii': True})