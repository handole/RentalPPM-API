from django.db import models


class master_uom(models.Model):
    uom_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'MasterUOM'

    def __str__(self):
        return self.name
