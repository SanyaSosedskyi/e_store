from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Category, Product, Order, OrderDetails
from accounts.models import UserProfileInfo
from django.contrib.auth.decorators import login_required


def catalog(request, category_id):
    categories = Category.objects.all()
    current_category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=current_category)
    context = {
        'categories': categories,
        'current_category': current_category,
        'products': products
    }
    return render(request, 'e_store/catalog.html', context)


def product(request, category_id, product_id):
    current_product = Product.objects.get(pk=product_id)
    error = ''
    product_description = current_product.description.split('\n')
    categories = Category.objects.all()
    if request.method == 'POST':
        if 0 <= int(request.POST.get('amount')) <= current_product.amount:
            if 'basket' not in request.session:
                request.session['basket'] = {}
            if str(product_id) not in request.session['basket']:
                request.session['basket'][str(product_id)] = int(request.POST.get('amount'))
            else:
                if not ((request.session['basket'][str(product_id)] + int(request.POST.get('amount')))
                        > current_product.amount):
                    request.session['basket'][str(product_id)] += int(request.POST.get('amount'))
                else:
                    error = 'Больше чем в наличии!'
            request.session.modified = True
            print(request.session['basket'])
        else:
            error = 'Некорректное значение!'
    return render(request, 'e_store/product.html', {'current_product': current_product,
                                                    'product_description': product_description,
                                                    'error': error,
                                                    'categories': categories})


@login_required
def basket(request):
    if request.user.is_authenticated and 'basket' not in request.session:
        request.session['basket'] = {}
        request.session.modified = True
    basket_ = {}
    if 'basket' in request.session:
        basket_ = request.session['basket']
    basket_ = request.session['basket']
    basket_modified = {}
    for b in basket_:
        basket_modified[b] = {
            'amount': basket_[b],
            'product': Product.objects.get(pk=b),
            'sum': basket_[b] * Product.objects.get(pk=b).price
        }
    order_total = 0
    for b in basket_modified:
        order_total += basket_modified[b]['sum']
    user_profile_info = UserProfileInfo.objects.get(user=request.user)
    if request.method == 'POST':
        order = Order()
        order.user = user_profile_info
        order.status = 'checking'
        order.total_sum = order_total
        order.address = request.POST.get('address')
        order.save()
        for item in basket_modified:
            order_detail = OrderDetails()
            order_detail.order = order
            order_detail.product = basket_modified[item]['product']
            order_detail.amount = basket_modified[item]['amount']
            order_detail.save()
            product_ = basket_modified[item]['product']
            product_.amount -= order_detail.amount
            product_.save()
        del request.session['basket']
        request.session.modified = True
    categories = Category.objects.all()
    return render(request, 'e_store/basket.html', {'basket_modified': basket_modified,
                                                   'categories': categories,
                                                   'order_total': order_total})


@login_required
def delete_from_basket(request, product_id):
    if str(product_id) in request.session['basket']:
        del request.session['basket'][str(product_id)]
        request.session.modified = True
    return redirect(reverse_lazy('e_store:basket'))


