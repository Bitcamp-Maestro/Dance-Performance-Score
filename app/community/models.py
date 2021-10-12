from django.db import models
from user.models import User

class Community(models.Model):
    PID = models.CharField(max_length=64, verbose_name='playID')
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=126, verbose_name = 'Title')
    isShared = models.CharField(max_length=40,verbose_name='Share')
    hastag = models.JSONField(max_length=300,verbose_name= 'Hashtag')
    views = models.CharField(max_length=10, verbose_name = 'Views')
    faves = models.CharField(max_length=10, verbose_name ='Likes')

    def __str__(self): 
        return self.PID 