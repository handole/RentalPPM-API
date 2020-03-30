from django.db import models
from .receiving_detail import receiving_detail


class receiving_detail_sn(models.Model):
    receiving_detail_sn_id = models.BigAutoField(primary_key=True)
    first_serial_number = models.CharField(max_length=100)
    new_serial_number = models.CharField(max_length=100, blank=True)
    receiving_detail_id = models.ForeignKey(receiving_detail, on_delete=models.CASCADE, blank=True, related_name='RDISN')

    class Meta:
        db_table = 'ReceivingDetailSN'

    def __str__(self):
        return str(self.receiving_detail_sn_id)
