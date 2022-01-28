from django.db import models


class Account(models.Model):
    balance = models.DecimalField(
        'Баланс', default=0,
        max_digits=12, decimal_places=2
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.id}'


class Accrual(models.Model):
    amount = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2
    )
    date = models.DateTimeField('Дата пополнения счета', auto_now_add=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='accrual', verbose_name='Счет'
    )
    description = models.TextField(
        'Описание пополнения', default='Пополнение счета'
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'

    def __str__(self):
        return (
            f'Счет номер {self.account.id} '
            f'был пополнен на {self.amount} руб.'
        )


class Debeting(models.Model):
    amount = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2
    )
    date = models.DateTimeField(
        'Дата списания денежных средств', auto_now_add=True
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='debeting', verbose_name='Счет'
    )
    description = models.TextField(
        'Описание списания', default='Списание со счета'
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Списание'
        verbose_name_plural = 'Списания'

    def __str__(self):
        return (
            f'Со счета номер {self.account.id} '
            f'списано {self.amount} руб.'
        )


class Transfer(models.Model):
    from_account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='from_account', verbose_name='Счет отправителя'
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='to_account', verbose_name='Счет получателя'
    )
    amount = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2
    )
    date = models.DateTimeField(
        'Дата перевода денежных средств', auto_now_add=True
    )
    description = models.TextField(
        'Описание перевода денежных средств',
        default='Перевод денежных средств'
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Перевод денежных средств'
        verbose_name_plural = 'Переводы денежных средств'

    def __str__(self):
        return (
            f'Перевод со счета {self.from_account} на счет {self.to_account}, '
            f'сумма перевода {self.amount} руб.'
        )
