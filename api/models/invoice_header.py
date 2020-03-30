from django.db import models

from .rental_register_header import rental_header


class invoice_header(models.Model):
    invoice_header_id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True)
    amount = models.CharField(max_length=100, blank=True)
    customer = models.BigIntegerField(blank=True)
    pay_method = models.IntegerField(blank=True)
    status = models.CharField(max_length=50, blank=True)
    rental_header_id = models.ForeignKey(rental_header, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'InvoiceHeader'

    def __str__(self):
        return str(self.invoice_header_id)
