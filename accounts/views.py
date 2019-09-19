from django.shortcuts import render, redirect
from .forms import UserProfileInfoForm, UserForm
from django.urls import reverse_lazy

def register(request):
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
            return redirect(reverse_lazy('e_store:catalog'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'accounts/register.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })


def login(request):
    pass