from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib import messages
from .models import Accelerator, Review
from .forms import ReviewForm

def reviews(request):
    context = {
        'accelerators': Accelerator.objects.all(),
        'reviews': Review.objects.all()
    }
    return render(request, 'reviews/reviews_home.html', context)

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/reviews_home.html'
    context_object_name = 'reviews'
    ordering = ['-date_posted']

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'

@login_required
def review_create(request, pk=None):
    accelerator = get_object_or_404(Accelerator, pk=pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_post = review_form.save(commit=False)
            new_post.author = request.user
            new_post.subject = accelerator
            new_post.save()
            return HttpResponseRedirect(new_post.get_absolute_url())
    else:
        review_form = ReviewForm()
    context = {
        'form': review_form
    }
    return render(request, 'reviews/review_form.html', context)

@login_required
def review_update(request, pk):
    post = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=post)
        if review_form.is_valid():
            updated_post = review_form.save(commit=False)
            updated_post.save()
            return HttpResponseRedirect(updated_post.get_absolute_url())
    else:
        review_form = ReviewForm(instance=post)
    context = {
        'form': review_form
    }
    return render(request, 'reviews/review_form.html', context)

def review_delete(request, pk=None):
    post = get_object_or_404(Review, pk=pk)
    post.delete()
    messages.success(request, f'Your review has been taken down.')
    return redirect(reverse('index'))

# Old create review view

#def review_create(request):
#    review_form = ReviewForm(request.POST or None)
#    if request.method == 'POST':
#        review_form = ReviewForm(request.POST)
#        if review_form.is_valid():
#            review_form.save()
#            Review.objects.create(**review_form.cleaned_data)
#            return redirect(reviews)
#    context = {
#        'form': review_form
#    }
#    return render(request, 'reviews/review_form.html', context)

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = "/"
    
    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False