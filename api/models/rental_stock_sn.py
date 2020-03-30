from django.db import models

from .rental_stock_card import rental_stock_card
from .receiving_detail_sn import receiving_detail_sn


class rental_stock_sn(models.Model):
    stock_code_id = models.BigAutoField(primary_key=True)
    first_sn = models.CharField(max_length=100)
    new_sn = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, blank=True)
    receiving_detail_sn_id = models.OneToOneField(receiving_detail_sn, on_delete=models.DO_NOTHING, null=True,
                                                  blank=True, related_name='StockSNFromRDSN')
    # RDSN stands for Receiving Detail SN
    stock_card_id = models.ForeignKey(rental_stock_card, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='StockSNFromRSC')

    # RSC stands for Rental Stock Card

    class Meta:
        db_table = 'RentalStockSN'

    def __str__(self):
        return str(self.stock_code_id)
