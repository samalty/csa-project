from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegisterForm
from reviews.models import Review

def index(request):
    reviews = Review.objects.all().order_by('-date_posted')[:4]
    context = {
        'reviews': reviews,
    }
    return render(request, 'accounts/index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome to your account, {username}')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})