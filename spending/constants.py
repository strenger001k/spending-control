from django.db import models


class SpendingCategory(models.TextChoices):
    car = "1", 'Авто'
    house = "2", 'Будинок'
    medicine = "3", 'Ліки'
    clothes = "4", 'Одяг'
    food = "5", 'Їжа'
    present = "6", 'Подарунки'
    travel = "7", 'Подорожі'
    tech = "8", 'Техніка'
    other = "9", "Інше"
