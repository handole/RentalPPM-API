from django.db import models


class master_location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=150)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'MasterLokasi'

    def __str__(self):
        return self.name
