from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = 'manager', 'Менеджер'
        ADMIN   = 'admin',   'Администратор'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
        verbose_name='Роль'
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_manager(self):
        return self.role == self.Role.MANAGER