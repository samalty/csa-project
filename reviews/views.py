from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from .models import Accelerator, Review
from .forms import ReviewForm, RawReviewForm

def reviews(request):
    context = {
        'accelerators': Accelerator.objects.all(),
        'reviews': Review.objects.all()
    }
    return render(request, 'reviews/reviews_home.html', context)

class AcceleratorListView(ListView):
    model = Accelerator
    template_name = 'reviews/accelerators_home.html'
    context_object_name = 'accelerators'
    ordering = ['-name']


def accelerator_detail(request, pk):
    accelerator = get_object_or_404(Accelerator, pk=pk)
    reviews = Review.objects.filter(subject=accelerator).order_by('-date_posted')[:3]
    context = {
        'accelerator': accelerator,
        'reviews': reviews,
    }
    return render(request, 'reviews/accelerator_detail.html', context)

def accelerator_reviews(request, pk):
    accelerator = get_object_or_404(Accelerator, pk=pk)
    reviews = Review.objects.filter(subject=accelerator).order_by('-date_posted')
    print(accelerator.name)
    print(len(reviews))
    context = {
        'accelerator': accelerator,
        'reviews': reviews,
    }
    return render(request, 'reviews/accelerator_reviews.html', context)


class AcceleratorCreateView(LoginRequiredMixin, CreateView):
    model = Accelerator
    fields = ['name', 'website', 'locations', 'bio', 'sector_focus', 'stage', 'deal', 'duration', 'logo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AcceleratorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Accelerator
    fields = ['name', 'website', 'locations', 'bio', 'sector_focus', 'stage', 'deal', 'duration', 'logo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # Test to ensure action can't be completed unless initiated by accelerator author
    def test_func(self):
        accelerator = self.get_object()
        if self.request.user == accelerator.author:
            return True
        return False

class AcceleratorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Accelerator
    success_url = "/"
    
    def test_func(self):
        accelerator = self.get_object()
        if self.request.user == accelerator.author:
            return True
        return False

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/reviews_home.html'
    context_object_name = 'reviews'
    ordering = ['-date_posted']

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'

#class ReviewCreateView(LoginRequiredMixin, CreateView):
#    model = Review
#    fields = ['subject', 'feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']
    
#    def form_valid(self, form):
#        form.instance.author = self.request.user
#        return super().form_valid(form)

def review_create(request):
    review_form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_post = review_form.save(commit=False)
            Review.objects.create(**review_form.cleaned_data)
            new_post.author = request.user
            new_post.save()
            #review_form.save()
            return redirect(reviews)
    context = {
        'form': review_form
    }
    return render(request, 'reviews/review_form.html', context)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = "/"
    
    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False