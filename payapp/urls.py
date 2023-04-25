from django.urls import path

from .views import (
    HomeTemplateView, TransactionListView, TransactionCreateView,
    TransactionRequestListView, TransactionRequestCreateView, TransactionRequestUpdateView,
    CurrencyConversionAPI, DashboardTemplateView, MoneyTemplateView, DepositView,EducationView,ConnectwithWallet

)


app_name = 'payapp'
urlpatterns = [

    # WEBSITE HOME PAGE
    path('', HomeTemplateView.as_view(), name='home'),
    path('deposit/<str:amount>/', DepositView.as_view(), name='deposit'),
    path('connect/', ConnectwithWallet.as_view(), name='wallet'),

    # USER DASHBOARD
    path('dashboard/', DashboardTemplateView.as_view(), name='dashboard'),
    path('money/', MoneyTemplateView.as_view(), name='money'),
    path('education/', EducationView.as_view(), name='education'),

    # TRANSACTIONS SERVICES
    path('transaction/', TransactionListView.as_view(), name='transactions'),
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction-create'),

    # REQUESTS SERVICES
    path('request/', TransactionRequestListView.as_view(), name='requests'),
    path('request/create/', TransactionRequestCreateView.as_view(), name='request-create'),
    path('request/<int:pk>/update/', TransactionRequestUpdateView.as_view(), name='request-update'),

    # API FOR CURRENCY CONVERSION
    path(
        'conversion/<str:currency1>/<str:currency2>/<str:amount>/',
        CurrencyConversionAPI.as_view(), name='currency-conversion-api'
    )

]
