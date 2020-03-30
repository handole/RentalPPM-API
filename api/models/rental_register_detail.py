from django.db import models

from .master_item import master_item
from .rental_register_header import rental_header
from .rental_order_detail import rental_order_detail


class rental_detail(models.Model):
    rental_detail_id = models.BigAutoField(primary_key=True)
    price = models.CharField(max_length=200)
    qty = models.IntegerField()
    discount_type = models.CharField(max_length=100, blank=True)
    discount_method = models.CharField(max_length=200, blank=True)
    discount = models.CharField(max_length=200, blank=True)
    total = models.CharField(max_length=200, blank=True)
    rental_header_id = models.ForeignKey(rental_header, on_delete=models.DO_NOTHING, blank=True, null=True,
                                         related_name='RentalDetailHeader')
    order_detail_id = models.OneToOneField(rental_order_detail, on_delete=models.DO_NOTHING, blank=True, null=True,
                                           related_name='RentalDetailROD')
    master_item_id = models.ForeignKey(master_item, on_delete=models.DO_NOTHING, blank=True, null=True,
                                       related_name='RentalDetailItems')

    class Meta:
        db_table = 'RentalDetail'

    def __str__(self):
        return str(self.rental_detail_id)

from .rental_stock_sn import rental_stock_sn
class rental_detail_sn(models.Model):
    rental_detail_sn_id = models.BigAutoField(primary_key=True)
    rental_detail_id = models.ForeignKey(rental_detail, on_delete=models.DO_NOTHING,null=True,blank=True, related_name='RDSN')
    stock_code_id = models.ForeignKey(rental_stock_sn, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return str(self.rental_detail_sn_id)