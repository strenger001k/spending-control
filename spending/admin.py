from django.contrib import admin

from spending.models import Spending


class SpendingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'date')


admin.site.register(Spending, SpendingAdmin)
