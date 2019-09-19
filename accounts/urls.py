from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/auth.html',
                                     redirect_authenticated_user='catalog/'), name='login'),
    path('logout/', LogoutView.as_view(template_name='e_store/catalog.html'), name='logout')
]