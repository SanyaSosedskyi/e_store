from django.shortcuts import render, redirect
from .forms import UserProfileInfoForm, UserForm, UserUpdateProfileInfoForm, UserUpdateForm
from django.urls import reverse_lazy
from .models import UserProfileInfo
from django.contrib.auth.decorators import login_required
from e_store.models import Order, OrderDetails, Product


def register(request):
    if not request.user.is_anonymous:
        return redirect(reverse_lazy('accounts:profile'))
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(reverse_lazy('e_store:catalog_redirect'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'accounts/register.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })


@login_required
def show_profile(request):
    user_profile_info = UserProfileInfo.objects.get(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserUpdateProfileInfoForm(request.POST, instance=user_profile_info)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user.set_password(user.password)
            user.save()
            profile = p_form.save()
            profile.save()
    orders = {}
    user_orders = Order.objects.filter(user=UserProfileInfo.objects.get(user=request.user))
    for item in user_orders:
        orders[str(item.id)] = {
            'order': item,
            'details': OrderDetails.objects.filter(order=item)
        }
    for o in orders:
        for item in orders[o]['details']:
            print(item)
    return render(request, 'accounts/profile.html', {'user_profile_info': user_profile_info,
                                                     'orders': orders})