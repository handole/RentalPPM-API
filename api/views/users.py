from django.http import Http404,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group, Permission

from api.models import master_customer, master_user
from api.models.master_employee import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.dispatch import receiver, Signal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from api.serializers import GroupSerializer, GroupPermission
import datetime

# This view is purposely used for testing only, improvement is considered and might used in further development

update_on_nested_serializer = Signal(providing_args=['test'])  # custom signal
update_on_rental_register = Signal(providing_args=['test'])  # custom signal 2
update_on_rental_order = Signal(providing_args=['test'])  # custom signal 3
todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')  # get current date

# Create your views here.
@api_view(['GET'])
def testView(request):
    return Response("Test")


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        employee, created = master_user.objects.get_or_create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'nama': user.username,
            'user_level':employee.user_level,
            'email': user.email
        })


class MasterUser(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        # iduser = self.get_object(pk)
        User.objects.filter(id=pk).update(is_active=False)
        master_user.objects.filter(user_id=pk).delete()
        return Response("Data pengguna berhasil dihapus", status=status.HTTP_201_CREATED)

class UserLevelPermission(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        employee,created = master_user.objects.get_or_create(user=user)
        permission = groupPermission.objects.filter(group_name=employee.user_level)
        a=[]
        for p in permission:
            b = {'kategori':p.kategori,'jenis_akses':p.jenis_akses}
            a.append(b)        
        return Response({
            'group_name':employee.user_level,
            "permissions":a
            })

class NestedGroup(APIView):
    def get(self, request, format=None):
        groupManagement = Group.objects.all()
        serializers = GroupSerializer(groupManagement, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = NestedStockCardSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class NestedGroupPermission(APIView):
    def get(self, request, pk, format=None):
        g_name = Group.objects.filter(id=pk).values('name')[0]['name']
        GPermission = groupPermission.objects.filter(group_name=g_name)
        a=[]
        for p in GPermission:
            b = {'kategori':p.kategori,'jenis_akses':p.jenis_akses}
            a.append(b)        
        return Response({
            'group_name':g_name,
            "permissions":a
            })

    def put(self, request, pk, format=None):
        status = request.data['status']
        if status == "update":            
            name = request.data['group_name']
            permission = request.data['permissions']
            cek_data = Group.objects.filter(name=name,id=pk).__len__()
            if cek_data == 1:                
                cek_GPermission = groupPermission.objects.filter(group_name=name).delete()
                for perm in permission:
                    groupPermission(group_name=name,kategori=perm['kategori'],jenis_akses=perm['jenis_akses']).save()
                respon = 'Hak akses berhasil di update'
            elif cek_data == 0:
                cek_name = Group.objects.filter(name=name).__len__()
                if cek_name == 1:
                    permission = request.data['permissions']
                    respon = 'Nama hak akses sudah digunakan'
                else:
                    Group.objects.filter(id=pk).update(name=name)
                    cek_GPermission = groupPermission.objects.filter(group_name=name).delete()
                    for perm in permission:
                        groupPermission(group_name=name,kategori=perm['kategori'],jenis_akses=perm['jenis_akses']).save()
                    respon = 'Hak akses berhasil di update'
        return Response({'status':respon})

