from django.shortcuts import render, redirect

#login_required: Access is prohibited unless the user is logged in
from django.contrib.auth.decorators import login_required

# require_http_methods: Specifies the type of request (GET or POST)
from django.views.decorators.http import require_http_methods

from .models import Cart, CartItem

# Verify that he is logged in, and if he is not registered, he goes to the page login
@login_required(login_url='login')


def cart_view(request):
    #use the filter method:
    cart = Cart.objects.filter(customer__user=request.user).first()

    if cart:
        cart_items = cart.items.all()
    else:
        cart_items = []
        cart = None



    # Calculate the total price of the cart items
    total_price = 0
    #A loop that goes through all the basket items and calculates the price
    # for the products inside the basket

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total_price += item.subtotal


    # Create a context dictionary to pass to the template
    context = {
        #cart_items: The items in the cart for the current user
        'cart_items': cart_items,
        #total_price: The total price of the cart items
        'total_price': round(total_price, 2),
        'cart': cart,
    }
    return render(request, 'cart/cart.html', context)



@login_required(login_url='login')
# Operations such as modifying or increasing the quantity must be POST for security reasons.
@require_http_methods(["POST"])

# Increase the quantity of a specific item in the cart
def increase_quantity(request, item_id):
    cart_item = CartItem.objects.filter(
        id=item_id,
        cart__customer__user=request.user
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_view')









@login_required(login_url='login')
# Operations such as modifying or increasing the quantity must be POST for security reasons.
@require_http_methods(["POST"])

def decrease_quantity(request, item_id):
    #We search for items in the CartItem table based on conditions:
    cart_item = CartItem.objects.filter(
        #The first condition id is the same as the required element
    id=item_id,
    #the second condition is that the cart belongs to the current user
    cart__customer__user=request.user
).first()
#Make sure the item already exists (not None):
    if cart_item and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart:cart_view')



@login_required(login_url='login')
# Operations such as modifying or increasing the quantity must be POST for security reasons.
@require_http_methods(["POST"])

def delete_item(request, item_id):
    cart_item = CartItem.objects.filter(
        id=item_id,
        cart__customer__user=request.user
    #If something is detected, stop and give the program an error
    #Returns only None
    ).first()

    if cart_item:
        cart_item.delete()

    return redirect('cart:cart_view')