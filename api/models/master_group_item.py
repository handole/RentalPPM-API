from django.db import models


class master_group_item(models.Model):
    group_id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'MasterGroupItem'

    def __str__(self):
        return self.name
