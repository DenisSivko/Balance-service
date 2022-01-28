import decimal

import requests
from django.conf import settings
from rest_framework import serializers

from .models import Account, Accrual, Transfer, Debeting


class AccountSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency')
        read_only_fields = ('id', 'balance', 'currency')


class AccountCurrencySerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField(
        method_name='currency_name'
    )
    balance = serializers.SerializerMethodField(
        method_name='currency_conversion'
    )

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency')
        read_only_fields = ('id', 'balance', 'currency')

    def currency_conversion(self, obj):
        request = self.context.get('request')
        currency = request.query_params.get('currency')
        account_id = request.data.get('id')
        account = Account.objects.get(id=account_id)
        response = requests.get(
            'https://freecurrencyapi.net/api/v2/latest?'
            f'apikey={settings.API_KEY}&base_currency=RUB'
        )
        currency_rate = response.json().get('data').get(currency)
        if currency_rate:
            balance = round(
                account.balance * decimal.Decimal(currency_rate), 2)
            return balance
        raise serializers.ValidationError(f'Валюты {currency} нет в списке!')

    def currency_name(self, obj):
        request = self.context.get('request')
        currency = request.query_params.get('currency')
        return currency


class AccrualSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)
    id = serializers.CharField(source='account')

    class Meta:
        model = Accrual
        fields = ('id', 'amount', 'currency', 'date')
        read_only_fields = ('date', 'currency')

    def create(self, validated_data):
        validated_data['account'].balance += validated_data['amount']
        validated_data['account'].save()
        return super().create(validated_data)


class DebitingSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)
    id = serializers.CharField(source='account')

    class Meta:
        model = Debeting
        fields = ('id', 'amount', 'currency', 'date')
        read_only_fields = ('date', 'currency')

    def create(self, validated_data):
        balance = validated_data['account'].balance
        amount = validated_data['amount']
        if amount < 0 or amount > balance:
            raise serializers.ValidationError('Недостаточно средств!')
        validated_data['account'].balance -= validated_data['amount']
        validated_data['account'].save()
        return super().create(validated_data)


class TransferSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)

    class Meta:
        model = Transfer
        fields = (
            'from_account', 'to_account', 'amount', 'currency', 'date'
        )


class TransactionSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(default='RUB', read_only=True)
    description = serializers.SerializerMethodField(
        method_name='description_transaction'
    )

    class Meta:
        model = Transfer
        fields = ('amount', 'currency', 'date', 'description')

    def description_transaction(self, obj):
        return str(obj)
