from django.db import models


class master_customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    customer_type = models.CharField(max_length=100)
    name = models.CharField(max_length=300, unique=True)
    address = models.CharField(max_length=500)
    pos_code = models.CharField(max_length=100, blank=True)
    phone_code = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    fax_code = models.CharField(max_length=50, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    mobile_phone = models.CharField(max_length=100, blank=True)
    pic_name = models.CharField(max_length=100, blank=True)
    pic_number = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'MasterCustomer'

    def __str__(self):
        return self.name
