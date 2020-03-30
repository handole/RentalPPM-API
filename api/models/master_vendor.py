from django.db import models


class master_vendor(models.Model):
    vendor_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)

    class Meta:
        db_table = 'MasterVendor'

    def __str__(self):
        return self.name
