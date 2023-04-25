from django.contrib import admin
from django.urls import path, include

from webapps2023.settings import ENVIRONMENT

urlpatterns = [
    path('admin/', admin.site.urls),
]

# your apps urls
urlpatterns += [
    path('', include('register.urls', namespace='register')),
    path('', include('payapp.urls', namespace='payapp')),
]

if ENVIRONMENT != 'server':
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls"))
    ]
