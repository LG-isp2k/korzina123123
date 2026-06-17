from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description', 'transaction_type']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Куда потратили?'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'transaction_type': 'Тип операции',
            'amount': 'Сумма (₽)',
            'description': 'Описание',
            'category': 'Категория',
        }