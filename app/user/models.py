from django.db import models

# Create your models here.
class User(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    username = models.CharField(max_length=64,verbose_name = '사용자명')
    password = models.CharField(max_length=64,verbose_name = '비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    
    def __str__(self): # 이 함수 추가
        return self.username  # User object 대신 나타낼 문자 


    class Meta:
        db_table = 'user'

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, blank =True)
    introduction = models.TextField(blank=True)
    image = ProcessedImageField(
    		blank = True,
        	upload_to = 'profile/images',
        	processors = [ResizeToFill(300, 300)],
        	format = 'JPEG',
        	options = {'quality':90},
    		)