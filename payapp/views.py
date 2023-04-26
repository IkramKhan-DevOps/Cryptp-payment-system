import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.response import Response
from .bll import total_request_amount, total_send_amount
from django.views.generic import ListView, DetailView, TemplateView

from payapp.models import Transaction, TransactionRequest
from payapp.utils import convert_crypto, convert_to_float
from register.models import User
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST
)
from register.models import User


class HomeTemplateView(TemplateView):
    template_name = 'payapp/home.html'


@method_decorator(login_required, name='dispatch')
class DashboardTemplateView(TemplateView):
    template_name = 'payapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(**kwargs)
        t_trans = Transaction.objects.filter(sender=self.request.user)
        transactions = Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        requests = TransactionRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        t_requests = TransactionRequest.objects.filter(receiver=self.request.user)
        context['total_send_amount'] = total_send_amount(self)
        context['total_request_amount'] = total_request_amount(self)
        context['t_trans'] = t_trans.count()
        context['t_requests'] = t_requests.count()
        context['recent_transactions'] = transactions[0:10]
        context['recent_requests'] = requests[0:10]
        context['total_transactions'] = transactions.count()
        context['total_amount'] = User.objects.get(id=self.request.user.id)
        return context


""" TRANSACTION VIEWS"""


@method_decorator(login_required, name='dispatch')
class TransactionListView(ListView):
    template_name = 'payapp/transactions.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Transaction.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        context['bitcoin'] = self.request.user.total_amount
        context['DOGE'] = convert_crypto(self.request.user.currency_type, 'DOGE', self.request.user.total_amount)
        context['ETHEREUM'] = convert_crypto(self.request.user.currency_type, 'ETHEREUM',
                                             self.request.user.total_amount)
        context['SHEBA'] = convert_crypto(self.request.user.currency_type, 'SHEBA', self.request.user.total_amount)
        return context


@method_decorator(login_required, name='dispatch')
class TransactionDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)),
            pk=self.kwargs['pk']
        )


@method_decorator(login_required, name='dispatch')
class TransactionCreateView(View):
    template_name = 'payapp/transaction_create.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        # IF: missing parameters
        if not email or not amount:
            messages.warning(request, "Email or Amount is missing")
            return redirect('payapp:transaction-create')

        receiver = User.objects.filter(email=email)

        # IF: no receiver
        if not receiver:
            messages.error(request, "User doesn't exists with this email address")
            return redirect('payapp:transaction-create')

        sender = request.user
        receiver = receiver[0]

        # IF: same user
        if receiver == sender:
            messages.warning(request, "You can't sent amounts to yourself")
            return redirect('payapp:transaction-create')

        # IF: amount issue
        if sender.total_amount <= float(amount):
            messages.warning(request, "In sufficient balance to perform this transaction")
            return redirect('payapp:transaction-create')

        # ADD: transaction
        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        receiver.total_amount += float(amount)
        receiver.save()
        sender.total_amount -= float(amount)
        sender.save()
        messages.success(request, "Amount Transferred successfully.")
        return redirect('payapp:transactions')


""" TRANSACTION REQUEST VIEWS"""


@method_decorator(login_required, name='dispatch')
class TransactionRequestListView(ListView):
    template_name = 'payapp/request_transaction_list.html'

    def get_queryset(self):
        return TransactionRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )


@method_decorator(login_required, name='dispatch')
class TransactionRequestDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(
            TransactionRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)),
            pk=self.kwargs['pk']
        )


@method_decorator(login_required, name='dispatch')
class TransactionRequestCreateView(View):
    template_name = 'payapp/request_transaction_create.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        # IF: no status parameter
        if not email or not amount:
            messages.warning(request, "Email or Amount is missing")
            return redirect('payapp:request-create')

        # IF: receiver not available
        request_from = User.objects.filter(email=email)
        if not request_from:
            messages.error(request, "User doesn't exists with this email address")
            return redirect('payapp:request-create')

        request_to = request.user
        request_from = request_from[0]

        # IF: same user
        if request_from == request_to:
            messages.warning(request, "You can't request amounts from yourself")
            return redirect('payapp:request-create')

        # SUCCESS: create transaction
        TransactionRequest.objects.create(sender=request_to, receiver=request_from, amount=amount)
        messages.success(request, "Your transactions request added successfully")
        return redirect('payapp:requests')


@method_decorator(login_required, name='dispatch')
class TransactionRequestUpdateView(View):

    def get(self, request, pk):

        # IF: no status parameter
        status = request.GET.get('status')

        # IF: get transaction or 404
        transaction_request = get_object_or_404(
            TransactionRequest.objects.filter(receiver=request.user, status='pending'), pk=pk
        )
        sender = transaction_request.receiver
        receiver = transaction_request.sender
        amount = transaction_request.amount

        # IF: wrong parameter
        if status not in ['approved', 'cancel']:
            messages.warning(request, "Some parameters are missing")
            return redirect('payapp:requests')

        if status == "cancel":
            transaction_request.status = "cancelled"
            transaction_request.checked_on = datetime.datetime.now()
            transaction_request.save()
            return redirect('payapp:requests')

        # IF: sender amount is less
        if amount > sender.total_amount:
            messages.warning(request, "In sufficient balance to perform this transaction")
            return redirect('payapp:requests', )

        # ADD: transaction
        Transaction.objects.create(
            sender=sender, receiver=receiver, amount=amount
        )

        # ADD: transaction
        Transaction.objects.create(
            sender=sender, receiver=receiver, amount=amount
        )

        # UPDATE: sender and receiver amounts
        sender.total_amount -= amount
        sender.save()
        receiver.total_amount += amount
        receiver.save()

        transaction_request.status = 'accepted'
        messages.success(request, "Request approved and transaction performed successfully")

        # UPDATE: request
        transaction_request.checked_on = datetime.datetime.now()
        transaction_request.save()

        # SUCCESS: message and redirect

        return redirect('payapp:requests')


@method_decorator(login_required, name='dispatch')
class MoneyTemplateView(TemplateView):
    template_name = 'payapp/money.html'


""" API """


@method_decorator(login_required, name='dispatch')
class CurrencyConversionAPI(APIView):
    def get(self, request, currency1, currency2, amount):

        # IF: currencies not supported
        if currency1 not in ['USD', 'EURO', 'GBP'] or currency2 not in ['USD', 'EURO', 'GBP']:
            return Response(
                status=HTTP_400_BAD_REQUEST, data={
                    'error': 'Only USD, EURO and GBP are supported'
                }
            )

        float_amount = convert_to_float(amount)

        # IF: not supported to convert into int or float
        if not float_amount:
            return Response(
                status=HTTP_400_BAD_REQUEST, data={
                    'error': 'Amount must be number (integer, float)'
                }
            )

        # IF: amount is less or equal to 0
        if float_amount <= 0:
            return Response(
                status=HTTP_200_OK, data={
                    'error': 'Amount must be numeric and greater than 0'
                }
            )

        # SUCCESS: everything is fine here
        converted_amount = convert_crypto(currency1, currency2, float_amount)
        return Response(
            status=HTTP_200_OK, data={
                'amount': converted_amount
            }
        )


@method_decorator(login_required, name='dispatch')
class DepositView(View):

    def get(self, request, amount, *args):
        user = User.objects.get(id=request.user.id)
        print(user.total_amount)
        user.total_amount += 10
        user.save()

        messages.success(request, "You have successfully deposited amoutn of " + str(amount))
        return redirect("payapp:dashboard")


class EducationView(TemplateView):
    template_name = 'payapp/education.html'


class ConnectwithWallet(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        user.is_connected = True
        user.save()
        messages.success(self.request, "Successfully connected with wallet")
        return redirect('payapp:dashboard')
