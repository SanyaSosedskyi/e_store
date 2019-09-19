from django.db import models
from django.core import validators
from accounts.models import UserProfileInfo
import uuid


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название',
                             validators=[validators.MinLengthValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


def upload_path(prefix, instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, ext.lower())
    return 'product_images/{filename}'.format(
        filename=filename
    )


def icon_upload_path(instance, filename):
    return upload_path('tag', instance, filename)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=50, verbose_name='Название',
                             validators=[validators.MinLengthValidator(3)])
    amount = models.IntegerField(verbose_name='Количество на складе', validators=[validators.MinValueValidator(5)])
    description = models.TextField(verbose_name='Описание',
                                   validators=[validators.MinLengthValidator(10)])
    image = models.ImageField(verbose_name='Изображение', upload_to=icon_upload_path)
    price = models.IntegerField(verbose_name='Цена', validators=[validators.MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    text = models.TextField(max_length=1000, verbose_name='Содержание комментария',
                            validators=[validators.MinLengthValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-created_at']

    def __str__(self):
        return self.id


class Order(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.PROTECT, verbose_name='Пользователь')
    STATUS_CHOICES = [
        ('checking', 'На рассмотрении'),
        ('sent', 'Отправлен'),
        ('canceled', 'Отменен'),
        ('done', 'Выполнен')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='checking', verbose_name='Статус')
    total_sum = models.IntegerField(verbose_name='Сумма заказа', validators=[validators.MinValueValidator(0)])
    address = models.CharField(max_length=200, verbose_name='Адрес доставки',
                               validators=[validators.MinLengthValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    updated_at = models.DateTimeField(verbose_name='Дата обновления заказа', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return self.id


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='order')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    amount = models.IntegerField(verbose_name='Кол-во единиц товара', validators=[validators.MinValueValidator(1)])

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Детали заказа'




