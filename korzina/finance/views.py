from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.urls import reverse  # <- ДОБАВЬТЕ ЭТУ СТРОКУ
from .models import Transaction, Category
from .forms import TransactionForm
from datetime import datetime

@login_required
def index(request):
    # Получаем все операции текущего пользователя
    transactions = Transaction.objects.filter(user=request.user)
    
    # Считаем баланс
    total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = round(total_income - total_expense, 2)
    total_income = round(total_income, 2)
    total_expense = round(total_expense, 2)
    
    # Данные для круговой диаграммы (расходы по категориям)
    expense_by_cat = (
        transactions.filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    
    # Подготовим списки для Chart.js (названия и суммы)
    categories_for_chart = [item['category__name'] for item in expense_by_cat if item['category__name'] is not None]
    amounts_for_chart = [float(item['total']) for item in expense_by_cat if item['category__name'] is not None]
    
    # Если данных нет, чтобы график не сломался
    if not categories_for_chart:
        categories_for_chart = ['Нет данных']
        amounts_for_chart = [1]

    # Форма для добавления новой записи
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_trans = form.save(commit=False)
            new_trans.user = request.user
            new_trans.save()
            return redirect(reverse('finance:index'))  # <- ИСПРАВЛЕННАЯ СТРОКА
    else:
        form = TransactionForm()

    context = {
        'balance': balance,
        'total_income': total_income,
        'total_expense': total_expense,
        'transactions': transactions[:10],
        'form': form,
        'categories': categories_for_chart,
        'amounts': amounts_for_chart,
    }
    return render(request, 'finance/index.html', context)