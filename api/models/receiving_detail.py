from django.db import models
from .receiving_header import receiving_header
from .master_item import master_item
from .master_uom import master_uom


class receiving_detail(models.Model):
    receiving_detail_id = models.BigAutoField(primary_key=True)
    qty = models.IntegerField()
    note = models.CharField(max_length=200, blank=True)
    receiving_header_id = models.ForeignKey(receiving_header, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RDHeader')
    master_item_id = models.ForeignKey(master_item, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RDItem')
    uom_id = models.ForeignKey(master_uom, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RDUom')

    class Meta:
        db_table = 'ReceivingDetail'

    def __str__(self):
        return str(self.receiving_detail_id)
