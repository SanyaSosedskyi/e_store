from django.shortcuts import render
from .models import Category, Product


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
    product_description = current_product.description.split('\n')
    return render(request, 'e_store/product.html', {'current_product': current_product,
                                                    'product_description': product_description})
