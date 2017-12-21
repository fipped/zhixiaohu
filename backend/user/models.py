from django.db import models
from django.contrib.auth.models import AbstractUser


# TODO add User to auth model
class User(AbstractUser):

    nickname = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.nickname


class UserService(object):
    @staticmethod
    def addUser(self, username, nickname, psw, email):
        if not self.exists(username):
            user = User.objects.create(username=username,  email=email, password=psw, nickname=nickname)
            user.save()
            return True
        return False

    @staticmethod
    def deleteUser(self, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def updateEmail(self, id, email):
        user = self.getUserByID(id)
        if user:
            user.email = email
            user.save()
            return True
        return False

    @staticmethod
    def updatePassword(self, id, psd):
        user = self.getUserByID(id)
        if user:
            user.set_password(psd)
            user.save()
            return True
        return False

    @staticmethod
    def exists(self, username):
        num = User.objects.filter(username=username).count()
        if num == 0:
            return False
        return True

    @staticmethod
    def getUserByUserName(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def getUserByID(self, id):
        try:
            user = User.objects.get(id=id)
            return user
        except User.DoesNotExist:
            return None

