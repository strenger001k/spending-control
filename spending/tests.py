from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from spending.models import Spending
from spending.statistics import StatisticsService


class StatisticTest(TestCase):
    def test_stats(self):
        now_date = timezone.now()
        price = {}
        price_user1 = {}

        user = User.objects.create_user('test1',
                                        'test1@gmail.com',
                                        'password123!@')

        user1 = User.objects.create_user('test2',
                                         'test2@gmail.com',
                                         'password123!@')

        # spending user
        Spending.objects.create(create_by=user,
                                name='Spend1_user',
                                price=100,
                                category='2')

        Spending.objects.create(create_by=user,
                                name='Spend2_user',
                                price=160,
                                category='4',
                                date=now_date-relativedelta(days=15))

        Spending.objects.create(create_by=user,
                                name='Spend3_user',
                                price=325,
                                category='1',
                                date=now_date-relativedelta(months=3))

        Spending.objects.create(create_by=user,
                                name='Spend4_user',
                                price=1000,
                                category='2',
                                date=now_date-relativedelta(years=10))

        # spending user1
        Spending.objects.create(create_by=user1,
                                name='Spend1_user1',
                                price=165,
                                category='6')

        #? statistics test user
        category_today, price['today'] = StatisticsService(user,
                                                           now_date-relativedelta(days=1),
                                                           now_date).run()
        category_month, price['month'] = StatisticsService(user,
                                                           now_date-relativedelta(months=1),
                                                           now_date).run()
        category_year, price['year'] = StatisticsService(user,
                                                         now_date-relativedelta(years=1),
                                                         now_date).run()
        category_all_time, price['all_time'] = StatisticsService(user).run()

        #? statistics test user1
        category_today_user1, price_user1['today'] = StatisticsService(user1,
                                                                       now_date-relativedelta(days=1),
                                                                       now_date).run()

        #! statistics test user
        price_test = {'today': 100,
                      'month': 260,
                      'year': 585,
                      'all_time': 1585}

        category_today_test = {'Авто': None,
                               'Будинок': 100,
                               'Ліки': None,
                               'Одяг': None,
                               'Їжа': None,
                               'Подарунки': None,
                               'Подорожі': None,
                               'Техніка': None,
                               'Інше': None}

        category_month_test = {'Авто': None,
                               'Будинок': 100,
                               'Ліки': None,
                               'Одяг': 160,
                               'Їжа': None,
                               'Подарунки': None,
                               'Подорожі': None,
                               'Техніка': None,
                               'Інше': None}

        category_year_test = {'Авто': 325,
                              'Будинок': 100,
                              'Ліки': None,
                              'Одяг': 160,
                              'Їжа': None,
                              'Подарунки': None,
                              'Подорожі': None,
                              'Техніка': None,
                              'Інше': None}

        category_all_time_test = {'Авто': [325, 1],
                                  'Будинок': [1100, 2],
                                  'Ліки': [None, 0],
                                  'Одяг': [160, 1],
                                  'Їжа': [None, 0],
                                  'Подарунки': [None, 0],
                                  'Подорожі': [None, 0],
                                  'Техніка': [None, 0],
                                  'Інше': [None, 0]}

        #! statistics test user1
        price_user1_test = {'today': 165}
        category_user1_today_test = {'Авто': None,
                                     'Будинок': None,
                                     'Ліки': None,
                                     'Одяг': None,
                                     'Їжа': None,
                                     'Подарунки': 165,
                                     'Подорожі': None,
                                     'Техніка': None,
                                     'Інше': None}
        #* user
        self.assertEqual(price_test, price)
        self.assertEqual(category_today_test, category_today)
        self.assertEqual(category_month_test, category_month)
        self.assertEqual(category_year_test, category_year)
        self.assertEqual(category_all_time_test, category_all_time)

        #* user1
        self.assertEqual(price_user1_test, price_user1)
        self.assertEqual(category_user1_today_test, category_today_user1)
