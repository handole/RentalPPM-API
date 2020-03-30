from django.db import models
from .master_item import master_item
from .rental_order_header import rental_order_header


class rental_order_detail(models.Model):
    order_detail_id = models.BigAutoField(primary_key=True)
    master_item_id = models.ForeignKey(master_item, on_delete=models.DO_NOTHING, blank=True)
    price = models.CharField(max_length=200)
    qty = models.IntegerField()
    discount_type = models.CharField(max_length=100, blank=True)
    discount_method = models.CharField(max_length=100, blank=True)
    discount = models.CharField(max_length=200, blank=True)
    total = models.CharField(max_length=200)
    sales_order_id = models.ForeignKey(rental_order_header, on_delete=models.DO_NOTHING, related_name='RODHeader', blank=True)

    class Meta:
        db_table = 'RentalOrderDetail'

    def __str__(self):
        return str(self.order_detail_id)
