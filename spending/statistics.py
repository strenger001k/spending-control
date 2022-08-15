from django.db.models import Sum
from django.utils import timezone

from spending.models import Spending
from spending.constants import SpendingCategory


class StatisticsService():
    def __init__(self, user, start_date: timezone = None, end_date: timezone = None):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        return self.get_full_report(self.start_date, self.end_date, self.user)

    def get_full_report(self, start_date: timezone, end_date: timezone, user):
        category = {}
        if not start_date and not end_date:
            for value, label in zip(SpendingCategory.values, SpendingCategory.labels):
                info = []
                prices = Spending.objects.filter(create_by=user, category=value) \
                                                  .values('category', 'price') \
                                                  .aggregate(Sum('price'))['price__sum']
                category_count = Spending.objects.filter(create_by=user, category=value).count()
                info.append(prices)
                info.append(category_count)
                category[label] = info

            price = Spending.objects.filter(create_by=user).values('category', 'price') \
                                    .aggregate(Sum('price'))['price__sum']
            return category, price

        for value, label in zip(SpendingCategory.values, SpendingCategory.labels):
            category[label] = Spending.objects.filter(create_by=user, category=value,
                                                      date__range=[start_date, end_date]) \
                                              .values('category', 'price') \
                                              .aggregate(Sum('price'))['price__sum']

        price = Spending.objects.filter(create_by=user,
                                        date__range=[start_date, end_date]) \
                                .values('category', 'price') \
                                .aggregate(Sum('price'))['price__sum']

        return category, price
