from django.db import models

from .receiving_detail import receiving_detail
from .receiving_header import receiving_header
from .rental_register_detail import rental_detail
from .rental_register_header import rental_header


class rental_stock_card(models.Model):
    stock_card_id = models.BigAutoField(primary_key=True)
    item_master_id = models.BigIntegerField()
    location_id = models.BigIntegerField()
    qty = models.IntegerField()
    rental_header_id = models.ForeignKey(rental_header, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RSCRenH')
    # RSCRenH stands for Rental Stock Card from Rental Header
    rental_detail_id = models.ForeignKey(rental_detail, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RSCRenD')
    # RSCRenH stands for Rental Stock Card from Rental Detail
    receiving_header_id = models.ForeignKey(receiving_header, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RSCRH')
    # RSCRenH stands for Rental Stock Card from Receiving Header
    receiving_detail_id = models.ForeignKey(receiving_detail, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RSCRD')
    # RSCRenH stands for Rental Stock Card from Receiving Detail

    class Meta:
        db_table = 'RentalStockCard'

    def __str__(self):
        return str(self.stock_card_id)
