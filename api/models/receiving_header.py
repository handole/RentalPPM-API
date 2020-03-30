from django.db import models
from .master_vendor import master_vendor
from .master_location import master_location
from .master_user import master_user


class receiving_header(models.Model):
    receiving_header_id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True)
    number = models.CharField(max_length=100, blank=True)
    number_preix = models.CharField(max_length=100, blank=True)
    counter = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True)
    approval1_date = models.DateField(blank=True, null=True)
    approval1 = models.BigIntegerField(blank=True, null=True)
    vendor_id = models.ForeignKey(master_vendor, on_delete=models.DO_NOTHING)
    location_id = models.ForeignKey(master_location, on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=300, blank=True)
    user_id = models.ForeignKey(master_user, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ReceivingHeader'

    def __str__(self):
        return str(self.receiving_header_id)
