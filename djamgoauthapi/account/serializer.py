from rest_framework import serializers
from account.models import User
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str, force_bytes
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegitsrationvSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password', 'write_only':True})
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs =  {
                'password':{'write_only': True}
        }

#validation passwaord and confirm password while registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise  serializers.ValidationError('password and Confirm password doesnot match')
        return attrs


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserloginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = ['id','email', 'name']



class UserPasswordSerializer(serializers.Serializer):
    password =serializers.CharField(max_length=200, style ={'input_type': 'password'}, write_only=True)
    password2 =serializers.CharField(max_length=200, style ={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user =self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password and password doesnot match')
        user.set_password(password)
        user.save()
        return attrs


class UserPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email =email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link ='http://127.0.0.1:8000/api/user/resent/'+uid+'/'+token
            print('hello......................................................................................' + link)
            body = 'resent your password by click this link '+link
            data = {'subject' :'reset Your Password',
                    'Body': body,  
                     'to_email': user.email }
            Util.send_email(data)
            return attrs
        else:
         raise serializers.ValidationError('you are not registertraion user  ') 
         


class UserPasswordSetSerializer(serializers.Serializer):
    password =serializers.CharField(max_length=200, style ={'input_type': 'password'}, write_only=True)
    password2 =serializers.CharField(max_length=200, style ={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid =self.context.get('uid')
        token =self.context.get('token')
                
        if password != password2:
            raise serializers.ValidationError('password and password doesnot match')
        id = smart_str(urlsafe_base64_decode(uid))
        user =User.objects.get(id = id)
        if not PasswordResetTokenGenerator().check_token(user,token):
             raise serializers.ValidationError('token is not valid or exprised')
        user.set_password(password)
        user.save()
        return attrs
       
               
        