from play.models import OptionForm, Option
from json.encoder import JSONEncoder
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template import context, loader
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class OptionView(TemplateView):
    template_name = 'option.html'

    def get(self, req, *args, **kwargs):

        print(req)
        template = loader.get_template(self.template_name)
        context = {'test':1}
        return HttpResponse(template.render(context, req))
    
    def post(self, req, *args,**kwargs):
        print('option recived')
        print(req.POST)
        print(req.FILES)
        # form = OptionForm(req.POST)
        # if form.is_valid() :
        #     form.save()
        
        play_option = Option(mode = req.POST['mode'], upload=req.POST['upload'], songs=req.POST['songs'], video=req.FILES['video'])
        play_option.save()

        return JsonResponse({
            'result': 200,
            }, json_dumps_params={'ensure_ascii': True})


class PlayView(TemplateView):
    template_name = 'play.html'
    
    def get(self, req, *args, **kwargs):
        print(req)
        template = loader.get_template('play.html')
        context = {'test':1}
        return HttpResponse(template.render(context, req))

    def post(self, req, *args, **kwargs):
        print(req)
        template = loader.get_template('play.html')
        context = {'test':1}
        return HttpResponse(template.render(context, req))


