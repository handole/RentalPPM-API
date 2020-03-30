from django.db import models
from .master_group_item import master_group_item
from .master_uom import master_uom
from .master_merk import master_merk


class master_item(models.Model):
    master_item_id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=100, blank=True)
    counter = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=200, unique=True)
    alias_name = models.CharField(max_length=200, blank=True)
    master_group_id = models.ForeignKey(master_group_item, on_delete=models.DO_NOTHING,related_name='MasterGroup')
    uom_id = models.ForeignKey(master_uom, on_delete=models.DO_NOTHING)
    merk_id = models.ForeignKey(master_merk, on_delete=models.DO_NOTHING)
    price1 = models.CharField(max_length=200)
    price2 = models.CharField(max_length=200, blank=True)
    price3 = models.CharField(max_length=200, blank=True)
    serial_number = models.BooleanField(default=True)

    class Meta:
        db_table = 'MasterItem'

    def __str__(self):
        return self.name
