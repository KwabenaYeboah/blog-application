from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from users.models import Profile

def register(request):
    if request.method =='POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Profile.objects.create(user=user)
            messages.success(request, f'Account created. You can Sign in now!')
            return redirect('sign_in')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form':form})
    
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                        instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'You have updated your account successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form':user_form, 'profile_form':profile_form
    }
    return render(request, 'users/profile.html', context)
 