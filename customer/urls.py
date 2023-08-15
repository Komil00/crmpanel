from django.urls import path
from .views import *
from .register import *

app_name = "customer"

urlpatterns = [
    path("register",RegisterView.as_view(), name="register"),
     path("activate",ActivateView.as_view(), name="activate"),
      path("auth",AuthorizationView.as_view(), name="auth"),

]