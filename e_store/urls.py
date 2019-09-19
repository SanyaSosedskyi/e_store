from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views
from .models import Category

app_name = 'e_store'

urlpatterns = [
    path('', RedirectView.as_view(url='{}/'.format(str(Category.objects.first().id))), name='catalog_redirect'),
    path('<int:category_id>/', views.catalog, name='catalog'),
    path('<int:category_id>/<int:product_id>/', views.product, name='product')
]