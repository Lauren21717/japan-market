from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('account/', views.account_detail, name='account_detail'),
    path('orders/', views.order_history_list, name="order_history_list"),
    path('orders/<order_number>', views.order_detail, name="order_detail"),
]
