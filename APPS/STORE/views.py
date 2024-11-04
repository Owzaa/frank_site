from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Order


'''
This code defines three views:

product_list: Displays a list of all products.
product_detail: Displays details of a specific product.
create_order: Handles the creation of an order via a POST request.

'''

def shop(request):
    return render(request,'shop/store.html')


def product(request):
    product = Product.objects.all()
    return render(request, 'store/products/product_list.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/products/product_detail.html', {'product': product})

def create_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, pk=product_id)
        order = Order(product=product, quantity=quantity)
        order.save()
        return JsonResponse({'message': 'Your Order created successfully', 'order_id': order.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)
