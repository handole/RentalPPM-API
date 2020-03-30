from django.core import serializers
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.forms import SignUpForm
from django.contrib.auth.models import User, Group, Permission
from api.models import *
from django.db.models import Q
from api.models.master_employee import *


@api_view(['POST'])
def signup(request):
    form = SignUpForm(request.data)
    print(request.data)
    if form.is_valid():
        user = form.save()        
        user.refresh_from_db()
        user.master_user.user_level = form.cleaned_data.get('user_level')
        user.master_user.user_type = form.cleaned_data.get('user_type')
        user.master_user.employee_id = master_employee(form.cleaned_data.get('employee_id'))
        user.save()
        return Response("Berhasil membuat account", status=status.HTTP_201_CREATED)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# Create or Edit Group
@api_view(['POST'])
def createGroup(request):
    group_name = request.data['group_name']
    permissions = request.data['permissions']
    group, created = Group.objects.get_or_create(name=group_name)
    for perm in permissions:
        if perm['kategori'] == "Manajemen Master":
            if perm['jenis_akses'] == "Hanya Lihat":
                listOfPermissions = Permission.objects.filter(name__contains="Can view master")
                for p in listOfPermissions:
                    if p.name == "Can view master_user" or p.name == "Can view master_employee":
                        continue
                    group.permissions.add(p)
            elif perm['jenis_akses'] == "Proses Data":
                listOfPermissions = Permission.objects.filter(name__contains="Can add master")
                for p in listOfPermissions:
                    if p.name == "Can add master_user" or p.name == "Can add master_employee":
                        continue
                    group.permissions.add(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can change master")
                for p in listOfPermissions:
                    if p.name == "Can change master_user" or p.name == "Can change master_employee":
                        continue
                    group.permissions.add(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can delete master")
                for p in listOfPermissions:
                    if p.name == "Can delete master_user" or p.name == "Can delete master_employee":
                        continue
                    group.permissions.add(p)
        elif perm['kategori'] == "Manajemen Inventori":
            if perm['jenis_akses'] == "Hanya Lihat":
                listOfPermissions = Permission.objects.filter(name__contains="Can view receiving")
                for p in listOfPermissions:
                    group.permissions.add(p)
            elif perm['jenis_akses'] == "Proses Data":
                listOfPermissions = Permission.objects.filter(name__contains="Can add receiving")
                for p in listOfPermissions:
                    group.permissions.add(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can change receiving")
                for p in listOfPermissions:
                    group.permissions.add(p)
                listOfPermissions = Permission.objeccts.filter(name__contains="Can delete receiving")
                for p in listOfPermissions:
                    group.permissions.add(p)
        elif perm['kategori'] == "Manajemen Kerja":
            if perm['jenis_akses'] == "Hanya Lihat":
                listOfPermissions = Permission.objects.filter(name__contains="Can view rental")
                for p in listOfPermissions:
                    group.permissions.add(p)
            elif perm['jenis_akses'] == "Proses Data":
                listOfPermissions = Permission.objects.filter(name__contains="Can add rental")
                for p in listOfPermissions:
                    group.permissions.add(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can change rental")
                for p in listOfPermissions:
                    group.permissions.add(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can delete rental")
                for p in listOfPermissions:
                    group.permissions.add(p)
        elif perm['kategori'] == "Manajemen Pengguna":
            if perm['jenis_akses'] == "Hanya Lihat":
                listOfPermissions = Permission.objects.filter(
                    Q(name__contains="Can view master_user") | Q(name__contains="Can view master_employee"))
                for p in listOfPermissions:
                    group.permissions.add(p)
            elif perm['jenis_akses'] == "Proses Data":
                listOfPermissions = Permission.objects.filter(
                    Q(name__contains="master_user") | Q(name__contains="master_employee"))
                for p in listOfPermissions:
                    if p.name == "Can view master_user" or p.name == "Can view master_employee":
                        continue
                    group.permissions.add(p)
    return Response("Berhasil membuat group!", status=status.HTTP_200_OK)

@api_view(['POST'])
def createNewGroup(request):
    group_name = request.data['group_name']
    permissions = request.data['permissions']
    group, created = Group.objects.get_or_create(name=group_name)
    cekPermissionGroup = groupPermission.objects.filter(group_name=group_name).__len__()
    if cekPermissionGroup == 0:
        for perm in permissions:
            groupPermission(group_name=group_name,kategori=perm['kategori'],jenis_akses=perm['jenis_akses']).save()
            result = "Berhasil membuat group baru"
    else:
        for perm in permissions:
            groupPermission.objects.filter(group_name=group_name,kategori=perm['kategori']).update(jenis_akses=perm['jenis_akses'])
            result = "Update permission "+group_name
    return Response(result, status=status.HTTP_200_OK)



# Remove permission from group
@api_view(['POST'])
def editGroup(request):
    group_name = request.data['group_name']
    group = Group.objects.get(name=group_name)
    jenis_akses = request.data['jenis_akses']
    kategori = request.data['kategori']
    jenis_aksi = request.data['jenis_aksi']

    k = 0
    ja = 0

    if jenis_akses == "Proses Data":
        ja = 2
    elif jenis_akses == "Hanya Lihat":
        ja = 1

    if kategori == "Manajemen Pengguna":
        k = 4
    elif kategori == "Manajemen Kerja":
        k = 3
    elif kategori == "Manajemen Inventori":
        k = 2
    elif kategori == "Manajemen Master":
        k = 1

    if jenis_aksi == "REMOVE":
        if k == 4:
            if ja == 1:
                listOfPermissions = Permission.objects.filter(
                    Q(name__contains="Can view master_user") | Q(name__contains="Can view master_employee"))
                for p in listOfPermissions:
                    group.permissions.remove(p)
            elif ja == 2:
                listOfPermissions = Permission.objects.filter(
                    Q(name__contains="master_user") | Q(name__contains="master_employee"))
                for p in listOfPermissions:
                    if p.name == "Can view master_user" or p.name == "Can view master_employee":
                        continue
                    group.permissions.remove(p)
        elif k == 3:
            if ja == 1:
                listOfPermissions = Permission.objects.filter(name__contains="Can view rental")
                for p in listOfPermissions:
                    group.permissions.remove(p)
            elif ja == 2:
                listOfPermissions = Permission.objects.filter(name__contains="Can add rental")
                for p in listOfPermissions:
                    group.permissions.remove(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can change rental")
                for p in listOfPermissions:
                    group.permissions.remove(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can delete rental")
                for p in listOfPermissions:
                    group.permissions.remove(p)
        elif k == 2:
            if ja == 1:
                listOfPermissions = Permission.objects.filter(name__contains="Can view receiving")
                for p in listOfPermissions:
                    group.permissions.remove(p)
            elif ja == 2:
                listOfPermissions = Permission.objects.filter(name__contains="Can add receiving")
                for p in listOfPermissions:
                    group.permissions.remove(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can change receiving")
                for p in listOfPermissions:
                    group.permissions.remove(p)
                listOfPermissions = Permission.objeccts.filter(name__contains="Can delete receiving")
                for p in listOfPermissions:
                    group.permissions.remove(p)
        elif k == 1:
            if ja == 1:
                listOfPermissions = Permission.objects.filter(name__contains="Can view master")
                for p in listOfPermissions:
                    if p.name == "Can view master_user" or p.name == "Can view master_employee":
                        continue
                    group.permissions.remove(p)
            elif ja == 2:
                listOfPermissions = Permission.objects.filter(name__contains="Can add master")
                for p in listOfPermissions:
                    if p.name == "Can add master_user" or p.name == "Can add master_employee":
                        continue
                    group.permissions.remove(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can change master")
                for p in listOfPermissions:
                    if p.name == "Can change master_user" or p.name == "Can change master_employee":
                        continue
                    group.permissions.remove(p)
                listOfPermissions = Permission.objects.filter(name__contains="Can delete master")
                for p in listOfPermissions:
                    if p.name == "Can delete master_user" or p.name == "Can delete master_employee":
                        continue
                    group.permissions.remove(p)
    return Response("Berhasil menghapus permission!", status=status.HTTP_200_OK)


# Get list of all group
@api_view(['GET'])
def getAllGroups(request):
    groups = Group.objects.all()
    data = serializers.serialize('json', groups)
    return HttpResponse(data, content_type='application/json')

@api_view(['GET'])
def getAllGroupsPermission(request):    
    permission = groupPermission.objects.all()
    data = serializers.serialize('json', permission)
    return HttpResponse(data, content_type='application/json')


@api_view(['POST'])
def getUser(request):
    user_name = request.data['name']
    user = User.objects.get(username=user_name)
    return Response("This functions works!", status=status.HTTP_200_OK)


@api_view(['POST'])
def assignGroupToUser(request):
    user_name = request.data['username']
    groups = request.data['groups']
    u = User.objects.get(username=user_name)

    for group in groups:
        g = Group.objects.get(name=group['name'])
        g.user_set.add(u)

    return Response("Berhasil menambahkan group ke user " + user_name, status=status.HTTP_200_OK)


@api_view(['POST'])
def removeGroupFromUser(request):
    user_name = request.data['username']
    groups = request.data['groups']
    u = User.objects.get(username=user_name)

    for g in groups:
        group_name = g['group_name']
        x = Group.objects.get(name=group_name)
        x.user_set.remove(u)

    return Response("Berhasil menghapus group dari user " + user_name, status=status.HTTP_200_OK)
