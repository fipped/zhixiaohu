from django.contrib import auth
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response

from user.models import User, UserService
from user.serializers import UserSerializer


def findUserByName(request):
    pass
    # data = request.query_params
    # name = data['name']
    # return Response()


def findUserById(request):
    data = request.query_params
    if 'user_id' not in data:
        return Response({
            'success': False,
            'msg': 'error in params'
        })
    id = data['user_id']
    user = UserService.getUserByID(id)
    if user:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    return Response({
        'success': True,
        'data': {}
    })


@require_http_methods(['POST'])
def register(request):
    data = request.data
    if not {'name', 'psd', 'email', 'studentID'}.issubset(set(data.keys())):
        return  Response({
            'success': False,
            'msg': 'bad params'
        })

    name = data['name']
    user = UserService.getUserByName(name)
    if not user:
        user = User.objects.create(name=data['name'],
                                   email=data['email'],
                                   studentId=data['studentID'])
        user.set_password(data['psd'])
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    else:
        return Response({
            'success': False,
            'msg': '用户名已被使用'
        })


def login(request):
    data = request.data
    if not {'name', 'psd'}\
            .issubset(set(data.keys())):
        return Response({
            'success': False,
            'msg': '参数错误'
        })
    name = data['name']
    psd = data['psd']
    user = auth.authenticate(username=name, password=psd)
    if user:
        seri = UserSerializer(user)
        auth.login(request, user)
        return Response({
            'success': True,
            # TODO let front end to modify code
            'data': seri.data
        })
    return Response({
        'success': False,
        'msg': '用户不存在or密码错误'
    })

# auth
def updateUser(request):
    pass

def deleteUser(request):
    pass
