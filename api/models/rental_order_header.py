from django.db import models
from .master_location import master_location
from .master_customer import master_customer
from .master_user import master_user


class rental_order_header(models.Model):
    sales_order_id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    number = models.CharField(max_length=100, blank=True)
    number_prefix = models.CharField(max_length=100, blank=True)
    counter = models.IntegerField(blank=True)
    tax = models.CharField(max_length=200, blank=True)
    discount_type = models.IntegerField(blank=True, null=True)
    discount = models.CharField(max_length=100, blank=True)
    delivery_fee = models.CharField(max_length=100, blank=True)
    amount = models.CharField(max_length=200)
    notes_kwitansi = models.CharField(max_length=300)
    salesman = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=100)
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    notes = models.CharField(max_length=500, blank=True)
    location_id = models.ForeignKey(master_location, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(master_customer, on_delete=models.DO_NOTHING)
    approved_by = models.BigIntegerField(blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    user_id = models.ForeignKey(master_user, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        db_table = 'RentalOrderHeader'

    def __str__(self):
        return str(self.sales_order_id)
