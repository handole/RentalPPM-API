from django.db import models

from .rental_stock_sn import rental_stock_sn
from .rental_register_header import rental_header


class stock_sn_history(models.Model):
    stock_sn_history_id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    status = models.CharField(max_length=50, blank=True)
    IncomingRef_id = models.BigIntegerField(null=True, blank=True)
    # RentalRef_id = models.BigIntegerField(null=True, blank=True)
    RentalRef_id = models.ForeignKey(rental_header, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='RentalHeader')
    stock_code_id = models.ForeignKey(rental_stock_sn, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='StockSNHistory')

    class Meta:
        db_table = 'StockSNHistory'

    def __str__(self):
        return str(self.stock_sn_history_id)
