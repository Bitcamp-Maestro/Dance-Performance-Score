from django.views.generic import TemplateView
from django.template import context, loader
from django.http import HttpResponse
from django.shortcuts import render, redirect

from server.settings import DB, BASE_DIR, PROJECT_DIR

import json

class ErrorView(TemplateView):
    template_name = 'error.html'

    def get(self, req):
        return render(req, self.template_name)

class TestView(TemplateView):
    template_name = 'test.html'

    def get(self, req):
      
        pid = 'PSMHCkITg6zRxOJhnlwH'
        # play_doc = DB.collection(u'Play').document(u'{}'.format(pid)).get()
        # play_doc1 = DB.collection(u'Play').document(pid).get()
        # play_doc2 = DB.collection(u'Play').document(u'PSMHCkITg6zRxOJhnlwH').get()
        # print(play_doc.to_dict())
        # print(play_doc1.to_dict())
        # print(play_doc2.to_dict())
        plays = DB.collection('Play').stream()
        user_list = []
        for play in plays:
            play_data = play.to_dict()
            user_data = play_data['user'].get().to_dict()
            user_list.append(user_data)

        for user in user_list:
            print(user)
            # data = play.to_dict()
            # user_ref = play['user']
            # print(user_ref.id)
            
            # play_data = play_ref.get().to_dict()

            # user_data = play_data['user'].get().to_dict()

        # render(req,self.template_name, {"day":day,"id":id,"projectname":projectname })
        return render(req, self.template_name)


class IndexView(TemplateView):
    
    template_name = 'index.html'
    def get(self, req):

        template = loader.get_template(self.template_name)
        context = {'req_id':1}
        return HttpResponse(template.render(context, req))

class StaticView(TemplateView):
    
    def get(self, req, static_name):
        if static_name == 'aboutus':
            return render(req, 'aboutus.html')
        elif static_name == 'introduce':
            return render(req, 'introduce.html')
        elif static_name == 'contactus':
            return render(req, 'contactus.html')
        else:
            return redirect('error')


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

        return render(req, self.template_name, {**play_data, 'user_name' : user_data['email']})

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


class RankingView(TemplateView):
    
    template_name = 'ranking.html'
    def get(self, req):
        user_data_list = []
        play_user_data_list = []
        ranking = {}
        upload_time = 0
        favorite = 0
        score = 0
        idx = 0
        user_doc = DB.collection('User').stream()
        play_doc = DB.collection('Play').stream()
        for pdoc in play_doc:
            play_data = pdoc.to_dict()
            play_user_data = play_data['user'].get().to_dict()
            play_user_data_list.append({
                "username" : play_user_data["username"],
                "faves" : play_data["faves"],
                "score" : float(play_data["total_score"])
                })
        # print(play_user_data_list)
        for udoc in  user_doc:
            idx += 1
            user_data = udoc.to_dict()
            
            # print(play_user_data["username"])
            for i in play_user_data_list:
                # print(i)
                if user_data["username"] == i["username"]:
                    upload_time += 1
                    favorite += i["faves"]
                    score += int(i["score"])
            # play_user_data_list.append(play_user_data)
            ranking[idx] = {
                # "image" : user_data['image_path'],
                "username" : user_data['username'],
                "uploadtime" : upload_time,
                "favorite" : favorite,
                "score" : score
            }

            user_data_list.append({
                "image" : user_data['image_path'],
                "username" : user_data['username'],
                "uploadtime" : upload_time,
                "favorite" : favorite,
                "score" : score
            })
            upload_time = 0
            favorite = 0
            score = 0

        # user_data_list_sorted = sorted(user_data_list.items(), reverse=True)
        context = {'rank_list': user_data_list}

        return render(req, 'ranking.html', context)

    def post(self, req):
        pass

