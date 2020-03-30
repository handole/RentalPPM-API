from django.db import models
from .master_employee import master_employee
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class master_user(models.Model):
    # user_id = models.BigAutoField(primary_key=True)
    # username = models.CharField(max_length=10, unique=True)
    # password = models.CharField(max_length=10)
    # last_login_date = models.DateField()
    # employee_id = models.OneToOneField(master_employee, on_delete=models.DO_NOTHING, blank=True, default=1)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_level = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10)
    employee_id = models.OneToOneField(master_employee, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'MasterUser'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        master_user.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.master_user.save()


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         master_user.objects.create(user=instance)
#     instance.master_user.save()
