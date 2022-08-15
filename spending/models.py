from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from spending.constants import SpendingCategory


class Spending(models.Model):
    create_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True, null=True,
                            verbose_name="Назва товару")
    price = models.IntegerField(blank=True, null=True, verbose_name="Витрати")
    category = models.CharField(max_length=10,
                                null=True,
                                blank=True,
                                choices=SpendingCategory.choices,
                                verbose_name="Категорія")

    comment = models.TextField(null=True, blank=True, verbose_name='Коментар')
    date = models.DateField(default=datetime.now, verbose_name="Дата")

    def __str__(self):
        return f'{self.create_by.username} - {self.price}'
