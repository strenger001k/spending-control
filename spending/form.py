from datetime import datetime

from django import forms

from spending.constants import SpendingCategory
from spending.models import Spending


class CreateSpendingForm(forms.Form):
    name = forms.CharField(max_length=255, label='Назва товару')
    price = forms.IntegerField(label='Витрати')
    category = forms.ChoiceField(label='Категорія',
                                 choices=SpendingCategory.choices)
    comment = forms.CharField(label='Коментар', required=False, max_length=255, widget=forms.Textarea)
    date = forms.DateField(initial=datetime.now, label='Дата')

    def save(self, user):
        new_spend = Spending.objects.create(
                create_by=user,
                name=self.cleaned_data['name'],
                price=self.cleaned_data['price'],
                category=self.cleaned_data['category'],
                comment=self.cleaned_data['comment'],
                date=self.cleaned_data['date']
        )
        return new_spend
