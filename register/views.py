from django.contrib.auth import login
from django.shortcuts import redirect, render

from register.forms import SignUpForm


def register_request(request):

    if request.user.is_authenticated:
        return redirect("payapp:dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect("register:cross-auth")
    else:
        form = SignUpForm()

    return render(request=request, template_name="register/signup.html", context={"form": form})


def cross_auth(request):

    if request.user.is_authenticated:
        return redirect("payapp:dashboard")
    else:
        return redirect("register:login")
