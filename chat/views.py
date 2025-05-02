from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Chat, Group
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class= RegisterSerializer


class LoginView(APIView):
    serializer_class= UserLoginSerializer

    def post(self, request, *args, **kwrgs):
        username= request.data.get('username')
        password= request.data.get('password')
        user= authenticate(username= username, password=password)

        if user is not None:
            refresh= RefreshToken.for_user(user)
            user_serializer= UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status= 401)
        

def index(request, group_name):
    print("Group Name", group_name)
    group= Group.objects.filter(name= group_name).first()
    chat= []
    if group:
        chats= Chat.objects.filter(group=group)
    else:
        group= Group(name= group_name)
        group.save()
    return render(request, 'chat/index.html', {'groupname':group_name, 'chats':chats})

