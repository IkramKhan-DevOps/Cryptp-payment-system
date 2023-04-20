from django.urls import path
from .views import HomeView, PrivacyPolicyView, TermsView


app_name = 'website'
urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms/', TermsView.as_view(), name='terms'),

]
