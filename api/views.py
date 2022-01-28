import decimal
from itertools import chain
from operator import attrgetter

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Account, Transfer
from .pagination import CustomPagination
from .serializers import (AccountCurrencySerializer, AccountSerializer,
                          AccrualSerializer, DebitingSerializer,
                          TransactionSerializer, TransferSerializer)


class BalanceViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    def get_queryset(self):
        account_id = self.request.data.get('id')
        account = Account.objects.filter(id=account_id)
        return account

    def get_serializer_class(self):
        query_params = self.request.query_params.get('currency')
        if query_params:
            return AccountCurrencySerializer
        return AccountSerializer


class AccountViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TransactionsViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        account = get_object_or_404(
            Account, id=self.request.data.get('id')
        )

        querysets = chain(
            account.accrual.all(), account.from_account.all(),
            account.to_account.all(), account.debeting.all()
        )
        query_params = self.request.query_params.get('ordering')

        if query_params:
            if query_params[0] == '-':
                result_list = sorted(
                    querysets, key=attrgetter(f'{query_params[1:]}'),
                    reverse=True
                )
                return result_list

            result_list = sorted(
                querysets, key=attrgetter(f'{query_params}')
            )
            return result_list

        return list(querysets)


class AccrualViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = AccrualSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account_id = self.request.data.get('id')

        try:
            account = Account.objects.get(id=account_id)
        except Exception:
            return Response(
                {'id': 'Укажите номер существующего счета!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(account=account)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class DebitingViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = DebitingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account_id = self.request.data.get('id')

        try:
            account = Account.objects.get(id=account_id)
        except Exception:
            return Response(
                {'id': 'Укажите номер существующего счета!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(account=account)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    serializer_class = TransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_account = Account.objects.get(
            id=self.request.data['from_account']
        )
        amount = self.request.data['amount']
        to_account = Account.objects.get(
            id=self.request.data['to_account']
        )

        if from_account == to_account:
            return Response(
                {'error': 'Получатель и отправитель совпадают!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                from_account.balance -= decimal.Decimal(amount)
                from_account.save()

                if from_account.balance < 0:
                    raise ValueError

                to_account.balance += decimal.Decimal(amount)
                to_account.save()

                Transfer.objects.create(
                    from_account=from_account,
                    to_account=to_account,
                    amount=amount
                )
        except ValueError:
            return Response(
                {'amount': 'Недостаточно средств '
                           'для перевода!'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
