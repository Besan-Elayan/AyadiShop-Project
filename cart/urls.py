from django.urls import path
from . import views 

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.delete_item, name='delete_item'),

]