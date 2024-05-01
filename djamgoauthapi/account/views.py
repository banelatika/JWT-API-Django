

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializer import *
from django.contrib.auth import authenticate
from account.renders import UserRenders
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



# Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegitsrationvView(APIView):
    renderer_classes = [UserRenders]
    def post(self, request, format = None):
        serializer = UserRegitsrationvSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token , 'msg':'registration Success'},status= status.HTTP_201_CREATED)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST )


class UserloginView(APIView):
    renderer_classes = [UserRenders]
    def post(self, request, format = None):
        serializer = UserloginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg':'login success'},status= status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors':['email or password not vaild']}}, status= status.HTTP_404_NOT_FOUND )


class UserprofileView(APIView):
    renderer_classes = [UserRenders]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None): 
       serializer =  UserProfileSerializer(request.user,) 

       return Response(serializer.data, status=status.HTTP_200_OK)   


class UserChangPpasswordView(APIView): 
    renderer_classes = [UserRenders]
    permission_classes = [IsAuthenticated]    
    def post(self, request, format =None):
        serilizer = UserPasswordSerializer( data= request.data, context = {'user': request.user}) 
        if serilizer.is_valid(raise_exception=True):
            return Response({'msg':'change success'}, status=status.HTTP_200_OK)  
        return Response(serilizer.errors, status= status.HTTP_400_BAD_REQUEST ) 

class SendPasswordResetEmailView(APIView): 
    renderer_classes = [UserRenders]
    def post(self, request, format =None):
        serilizer = UserPasswordResetEmailSerializer(data =request.data)
        if serilizer.is_valid(raise_exception=True):
             return Response({'msg':'password link send on ur Email ID'}, status=status.HTTP_200_OK)  
        


class SendPasswordResetView(APIView): 
    renderer_classes = [UserRenders]
    def post(self, request, uid, token, format =None):
        serilizer = UserPasswordSetSerializer(data = request.data , context = {'uid' : uid ,'token ':token})
        if serilizer.is_valid(raise_exception=True):
            return Response({'msg':'password chnaged by emaild'}, status=status.HTTP_200_OK) 
        return Response(serilizer.errors, status= status.HTTP_400_BAD_REQUEST )