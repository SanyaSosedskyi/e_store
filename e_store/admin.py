from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'price', 'amount')
    search_fields = ('title', 'category')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'total_sum', 'address', 'get_order_products')
    search_fields = ('user', 'status', 'address')

    def get_order_products(self, obj):
        string = ''
        order_details_objs = models.OrderDetails.objects.filter(order=obj)[:5]
        for item in order_details_objs:
            string += item.product.title + ' = ' +  str(item.amount) + 'шт.; \n'
        return string

    get_order_products.short_description = 'Товары'


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'amount', 'get_user', 'get_total_sum')
    search_fields = ('order', 'product', 'get_user')

    def get_user(self, obj):
        return obj.order.user

    def get_total_sum(self, obj):
        return obj.amount * obj.product.price

    get_total_sum.short_description = 'Сумма'
    get_user.short_description = 'Пользователь'


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderDetails, OrderDetailsAdmin)
# Register your models here.
