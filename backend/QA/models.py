from django.db import models

# Create your models here.
from user.models import User


class Topic(models.Model):
    name = models.CharField(max_length=20)
    watches = models.ManyToManyField(to=User, related_name='watches')

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)
    title = models.CharField(u"标题", max_length=100)
    detail = models.CharField(u"描述", max_length=1000)
    watches = models.ManyToManyField(to=User, related_name='watches')
    topic = models.ManyToManyField(to=Topic, related_name='话题')


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    stared = models.ManyToManyField(to=User, related_name='started')
    approve = models.IntegerField(u"赞同数", default=0)
    against = models.IntegerField(u"反对数", default=0)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)
    detail = models.CharField(u"描述", max_length=1000)


class Image(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE, null=True)
    is_answer = models. BooleanField()
    url = models.ImageField()
