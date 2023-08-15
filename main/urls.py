from django.urls import path
from .views import *


app_name = "main"

urlpatterns = [
    path("categories",category_api_view, name="category_api_view"),
    path("category/<int:pk>/services",category_detail_view, name="category_detail_view"),
    path("service/<int:pk>",service_detail_view, name="service_detail_view"),

]