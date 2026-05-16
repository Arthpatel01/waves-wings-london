from django.contrib.auth.models import AbstractUser
from django.db import models
from base_models import BaseModel


class User(AbstractUser, BaseModel):
    """
    Custom User Model - Django automatically creates 'id' as primary key
    """
    # ❌ REMOVE: user_id = models.AutoField(primary_key=True)
    # Django automatically creates: id = models.AutoField(primary_key=True)

    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('viewer', 'Viewer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    class Meta:
        db_table = 'app_user'

    def __str__(self):
        return f"{self.username} (ID: {self.id})"  # Use 'id', not 'user_id'