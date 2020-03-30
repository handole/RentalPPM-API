from django.contrib.auth.models import User
from django.db import models


class master_employee(models.Model):
    employee_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=300)
    id_type = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    employee_status = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.CharField(max_length=50)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'MasterEmployee'

    def __str__(self):
        return self.name

class groupPermission(models.Model):
    group_name = models.CharField(max_length=100,null=True,blank=True)
    kategori = models.CharField(max_length=100,null=True,blank=True)
    jenis_akses = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.kategori
