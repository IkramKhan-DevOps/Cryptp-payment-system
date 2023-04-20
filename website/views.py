import os

from django.shortcuts import render
from django.views import View


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name)


class HomeView(View):

    def get(self, request):

        def convert_fullname_to_shortname(full_name):
            if full_name == 'bitcoin':
                return 'BTC'
            elif full_name == 'ethereum':
                return 'ETH'
            else:
                return 'DOGE'

        import requests

        # define the list of cryptocurrencies
        cryptos = ["bitcoin", "ethereum", "dogecoin"]

        # make the API request
        response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(cryptos)}&vs_currencies=usd")

        # get the data from the response
        data = response.json()

        context = {}
        for crypto in cryptos:
            context[convert_fullname_to_shortname(crypto)] = data[crypto]['usd']

        return render(request, 'website/home.html', context)


class PrivacyPolicyView(View):

    def get(self, request):
        return render(request, 'website/privacy-policy.html')


class TermsView(View):

    def get(self, request):
        return render(request, 'website/terms.html')
