from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AccountViewSet, AccrualViewSet, BalanceViewSet,
                    DebitingViewSet, TransactionsViewSet, TransferViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'account',
    AccountViewSet, basename='account'
)
router_v1.register(
    'accrual',
    AccrualViewSet, basename='accrual'
)
router_v1.register(
    'balance',
    BalanceViewSet, basename='balance'
)
router_v1.register(
    'debiting',
    DebitingViewSet, basename='debiting'
)
router_v1.register(
    'transfer',
    TransferViewSet, basename='transfer'
)
router_v1.register(
    'transactions',
    TransactionsViewSet, basename='transactions'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
