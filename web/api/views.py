import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from web.models import Signup, apartment, apartments
from .serializers import SignupSerializer


class SignupAPIView(generics.CreateAPIView):
    queryset = Signup.objects.all()
    serializer_class = SignupSerializer

    def GenerateSecurityCode(self, limit=6):
        limit = int(limit)
        code = ''
        for i in range(0,limit):
            x = random.randint(0,9)
            x = str(x)
            code += x
        return code
    def DeleteLast(self, phonenumber):
        phonenumber = str(phonenumber)
        items = Signup.objects.filter(phonenumber=phonenumber)
        for item in items:
            item.delete()
        return True
    def perform_create(self, serializer):
        self.DeleteLast(str(serializer.validated_data.get('phonenumber')))
        code = self.GenerateSecurityCode()
        obj = serializer.save(security_code=code)
        self.object_pk = obj.pk

    def create(self, request, *args, **kwargs):
        response = super(SignupAPIView, self).create(request, args, kwargs)
        response.data['status'] = 'ok'
        response.data['api-path'] = '/signup/security-code/%s/'%(self.object_pk)
        return response


class VerifyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        if request.POST.has_key('security-code'):
            code = request.POST['security-code']
            pk = kwargs.get('pk')
            obj = get_object_or_404(Signup, pk=pk)
            phonenumber = str(obj.phonenumber)
            if code == str(obj.security_code):
                user = User.objects.create(username=phonenumber)
                token = Token.objects.create(user=user)
                data['status'] = 'ok'
                data['verify'] = 'true'
                data['token'] = str(token.key)

            else:
                data['status'] = 'fail'
                data['verify'] = 'false'
        else:
            data['status'] = 'fail'
            data['detail'] = 'bad arguments'
        
        return Response(data=data)

class CompleteProfile(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        if request.META.has_key('HTTP_AUTHORIZATION'):
            if request.POST.has_key('first-name') and request.POST.has_key('last-name') and request.POST.has_key('el-area') and request.POST.has_key('count-family') :
                first_name = request.POST.get('first-name')
                last_name = request.POST.get('last-name')
                el_area = request.POST.get('el-area')
                count_family = request.POST.get('count-family')
                token = request.META.get('HTTP_AUTHORIZATION')
                token = str(token)
                token = token[6:]
                print token
                user = get_object_or_404(User,auth_token__key=token)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                apartment.objects.create(user=user, el_area=el_area, count_family=count_family)
                data['status'] = 'ok'
                data['profile-updated'] = 'true'
                data['first-name'] = first_name
                data['last-name']  = last_name
                data['el-area'] = el_area
                data['count-family'] = count_family

            else:
                data['status'] = 'fail'
                data['detail'] = 'bad arguments'

        else:
            data['status'] = 'fail'
            data['detail'] = 'missing Authorization token'

        return Response(data=data)


class CreateApartmentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        if request.META.has_key('HTTP_AUTHORIZATION'):
            if request.POST.has_key('create'):
                create = request.POST.get('create')
                if create:
                    token = request.META.get('HTTP_AUTHORIZATION')
                    token = str(token)
                    token = token[6:]
                    user = get_object_or_404(User,auth_token__key=token)
                    this_apartment = apartment.objects.get(user=user)
                    apartments.objects.create(admin_apartment=this_apartment)
                    data['status'] = 'ok'
                    data['created'] = 'true'
            else:
                data['status'] = 'fail'
                data['detail'] = 'bad atgument'

        else:
            data['status'] = 'fail'
            data['detail'] = 'missing Authorization token'
        return Response(data=data)
        