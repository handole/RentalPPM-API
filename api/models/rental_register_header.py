from django.db import models

from .master_customer import master_customer
from .master_location import master_location
from .master_user import master_user
from .rental_order_header import rental_order_header


class rental_header(models.Model):
    rental_header_id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    user_id = models.ForeignKey(master_user, on_delete=models.DO_NOTHING, null=True, blank=True)
    number = models.CharField(max_length=100, blank=True)
    number_prefix = models.CharField(max_length=100, blank=True)
    counter = models.IntegerField(blank=True)
    discount_type = models.IntegerField(blank=True, null=True)
    discount = models.CharField(max_length=100, blank=True)
    tax = models.CharField(max_length=200, blank=True)
    delivery_cost = models.CharField(max_length=100, blank=True)
    amount = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    salesman = models.BigIntegerField(blank=True, null=True)
    notes_kwitansi = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=100)
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    sales_order_id = models.OneToOneField(rental_order_header, on_delete=models.DO_NOTHING, null=True, blank=True)
    customer_id = models.ForeignKey(master_customer, on_delete=models.DO_NOTHING)
    location_id = models.ForeignKey(master_location, on_delete=models.DO_NOTHING)
    approved_by = models.BigIntegerField(blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    pay_type = models.IntegerField()
    pay_method = models.IntegerField(default=None)
    note_kwitansi = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'RentalHeader'

    def __str__(self):
        return str(self.rental_header_id)
