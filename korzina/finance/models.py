from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Категория трат (еда, транспорт, развлечения)"""
    name = models.CharField('Название', max_length=100)
    # Иконка категории - загружаем картинку
    icon = models.ImageField('Иконка', upload_to='category_icons/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Transaction(models.Model):
    """Операция (доход или расход)"""
    TYPE_CHOICES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    description = models.CharField('Описание', max_length=255)
    transaction_type = models.CharField('Тип', max_length=7, choices=TYPE_CHOICES)
    date = models.DateTimeField('Дата', auto_now_add=True)  # Запоминает время создания
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} руб."

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date']  # Сначала новые