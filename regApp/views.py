from django.shortcuts import render
from rest_framework import generics
from .models import NewUser
from .serializers import RegistrationSerializer,ChangePasswordSerializer
from django.utils import timezone
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny,IsAuthenticated

from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login as auth_login
# Create your views here.

class UserCreate(generics.GenericAPIView):
    queryset = NewUser.objects.all()
    serializer_class = RegistrationSerializer


    def post(self, request, *args, **kwargs):
        #data = JSONParser().parse(request)
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        user = serializer.save()
        #user =NewUser.objects.create_user(request['email'], request['first_name'], request['password'], request['last_name'], request['mobile'])
        token = Token.objects.create(user= user)
        #return Response(token)
        return JsonResponse({'token': str(token)}, status= 200)


class LoginAPI(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        auth_login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = NewUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset= None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data= request.data)

        if serializer.is_valid():
            # We are checking the old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set new password and also returnn to user
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)