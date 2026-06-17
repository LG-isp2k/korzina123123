from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    list_display_links = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_type', 'category', 'amount', 'description', 'date')
    list_filter = ('transaction_type', 'category', 'date')  # Фильтры справа
    search_fields = ('description',)  # Поиск по описанию
    date_hierarchy = 'date'  # Удобная навигация по датам
    list_display_links = ('description',)