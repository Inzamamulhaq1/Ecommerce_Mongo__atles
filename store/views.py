from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegisterForm
from .models import Product


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    return render(request, 'product_detail.html', {'product': product})


  
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Ensure the quantity is provided in the POST request
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        
    else:
        # Handle session-based cart for anonymous users
        # You can implement session-based cart handling here

        # Example session handling (basic)
        if quantity > product.stock_quantity:
        # Handle the case where requested quantity exceeds available stock
            return render(request, 'product_detail.html', {
                'product': product,
                'error_message': 'Requested quantity exceeds available stock.'
            })

        cart = request.session.get('cart', {})
        
        if str(product.pk) in cart:
            cart[str(product.pk)]['quantity'] += quantity
            print(cart)
        else:
            cart[str(product.pk)] = {'quantity': quantity, 'price': str(product.price)}
        request.session['cart'] = cart
        return redirect('product_list')
    
    cart_item.quantity += quantity
    cart_item.save()
    messages.success(request, 'Your Product has Added to Cart')
    return redirect('cart_view')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart_view.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, pk):
    """
    Remove a specific item from the user's cart.
    """
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=pk)
    cart_item.delete()
    messages.success(request, 'Item has been removed from the cart.')
    return redirect('cart_view')



@login_required
def clear_cart(request):
    """
    Remove all items from the user's cart.
    """
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, 'All items have been removed from your cart.')
    return redirect('cart_view')


@login_required
def order_list(request):
    # Retrieve orders with products for the current user
    orders = Order.objects.filter(user=request.user, total_price__gt=0).prefetch_related('products__product')
    # for order in orders:
    #     for item in order.products.all():
    #         print(item.product)
        
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def order_summary(request):
    # Retrieve all items in the user's cart
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)

    # Create an Order instance with the total price
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.products.set(cart_items)
    order.save()

    # Update the stock quantity of each product in the cart
    for item in cart_items:
        item.product.stock_quantity -= item.quantity
        item.product.save()

    # Clear the cart after creating the order
    cart_items.delete()
    

    return render(request, 'order_summary.html', {'order': order})


def singleOrder(request,pk):
    cart_items = CartItem.objects.filter(user=request.user,product_id=pk)
    total_price = sum(item.total_price for item in cart_items)
    print(cart_items)
    print(total_price)
    
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.products.set(cart_items)
    order.save()
    
    for item in cart_items:
        item.product.stock_quantity -= item.quantity
        item.product.save()
        
    cart_items.delete()
    
    
    return render(request, 'singleorder.html',{'order': order})
    


class logoutView(View):
    def get(self,request):
        logout(request)
        return render(request,'logout.html')
    
class registerView(View):
    def get(self,request):
        
        form = UserRegisterForm()
        context = {
            'form':form
            }
        return render(request,'register.html',context)
    
    def post(self,request):
        
        form = UserRegisterForm(request.POST)
        print(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Successfully created for {username}')
            return redirect('login')
        return render(request,'register.html',{'form':form})
  
