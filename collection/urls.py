from django.urls import path
from . import views

urlpatterns = [
    path('', views.collection, name='collection'),
    path('<product_id>', views.product_detail, name='product_detail'),
]
