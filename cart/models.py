from django.db import models
from accounts.models import Customer
#from products.models import Product


# Cart model (OneToOne with Customer)
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for - {self.customer.user.username}"


# CartItem model (Many items per Cart, each item linked to one Product)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    #product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CartItem: {self.product.name} - quantity: {self.quantity}"