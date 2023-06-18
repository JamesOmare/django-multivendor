from audioop import add
from re import T
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
from requests import session
import stripe
from django.http import JsonResponse

from .cart import Cart
from .models import Order, Product, Category, OrderItem
from .forms import OrderForm



def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')


def change_quantity(request, product_id):
    action = request.GET.get('action', None)
    
    if action:
        quantity = 1
        
        if action == 'decrease':
            quantity = -1
        
        cart = Cart(request)
        cart.add(product_id, quantity, True)


    return redirect('cart_view')


def remove_from_cart(request, product_id):  
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html', {
        'cart': cart
    })
    
@login_required
def checkout(request):
    cart = Cart(request)
    
    if cart.get_total_cost() == 0:
        return redirect('cart_view')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        zipcode = data['zipcode']
        city = data['city']
        
        if first_name and last_name and address and zipcode and city:
            form = OrderForm(request.POST)
            
            total_price = 0
            items = []
            
            for item in cart:
                product = item['product']
                total_price += product.price * item['quantity']                
                
                items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.title,
                        },
                        'unit_amount': product.price,
                    },
                    'quantity': item['quantity'],
                })

            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            try:
                session = stripe.checkout.Session.create(
                    line_items = items,
                    mode='payment',
                    success_url= settings.WEBSITE_URL + 'cart/success/',
                    cancel_url= settings.WEBSITE_URL + 'cart/',
                )
            except Exception as e:
                print("Exception while creating stripe session: ", str(e))
                return {'msg':'something went wrong while creating stripe session','error':str(e)}
            
            else:
                print(f'session_id: {session.id}')
                
                try:
                    payment_intent = stripe.PaymentIntent.create(
                            amount= total_price,
                            currency="usd",
                            payment_method_types=["card"],
                            )
                except Exception as e:
                    payment_intent = None
                    print("Exception while creating stripe payment intent: ", str(e))
                    return {'msg':'something went wrong while creating stripe payment intent','error':str(e)}
                else:
                    print(f'payment intent: {payment_intent.id}')
                
                order = Order.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    address = address,
                    zipcode = zipcode,
                    city = city,
                    created_by = request.user,
                    is_paid = True,
                    payment_intent = payment_intent.id,
                    paid_amount = total_price
                )
                
                
                for item in cart:
                    product = item['product']
                    quantity = int(item['quantity'])
                    price = product.price * quantity
                    
                    item = OrderItem.objects.create(order = order, product = product, quantity = quantity, price = price)

                cart.clear()
                
            return JsonResponse({'session_id': session.id})
            
        
    else:
        form = OrderForm() 
    
    
    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
        }
    )


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status = Product.ACTIVE).filter(
        Q(title__icontains = query) | Q(description__icontains = query)
    )
    context = {
        'query': query,
        'products': products
    }

    return render(request, 'store/search.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug = slug)
    products = category.products.filter(status = Product.ACTIVE)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/category_detail.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)


def success(request):
    return render(request, 'store/success.html')