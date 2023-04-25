from payapp.models import Transaction, TransactionRequest


def total_send_amount(self):
    trans = Transaction.objects.filter(sender=self.request.user)
    amount = 0
    for i in trans:
        amount += i.amount
    return amount


def total_request_amount(self):
    trans = Transaction.objects.filter(sender=self.request.user)
    amount = 0
    for i in trans:
        amount += i.amount
    return amount
