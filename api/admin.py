from django.contrib import admin

from .models import Account, Accrual, Transfer, Debeting

EMPTY_VALUE = '-пусто-'


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance')
    search_fields = ('id',)
    list_filter = ('id', 'balance')
    empty_value_display = EMPTY_VALUE


@admin.register(Accrual)
class AccrualAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'account')
    search_fields = ('account',)
    list_filter = ('date', 'account')
    empty_value_display = EMPTY_VALUE


@admin.register(Debeting)
class DebetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'account')
    search_fields = ('account',)
    list_filter = ('date', 'account')
    empty_value_display = EMPTY_VALUE


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_account', 'to_account', 'amount', 'date')
    search_fields = ('from_account', 'to_account')
    list_filter = ('date', 'from_account', 'to_account')
    empty_value_display = EMPTY_VALUE
