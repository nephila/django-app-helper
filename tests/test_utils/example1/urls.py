from django.urls import path

from .views import hello

urlpatterns = [path("/hello", hello, name="hello")]  # NOQA
