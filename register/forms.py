from django.contrib.auth.forms import UserCreationForm

from payapp.utils import convert_crypto
from register.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'currency_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.total_amount = convert_crypto("BTC", self.cleaned_data.get('currency_type'),10)
        print(self.cleaned_data.get('currency_type'))
        print(convert_crypto("BTC", self.cleaned_data.get('currency_type'),10))
        if commit:
            user.save()
        return user