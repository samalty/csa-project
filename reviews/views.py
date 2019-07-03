from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .models import Accelerator, Review

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
    ordering = ['-overall_rating']

#class AcceleratorDetailView(DetailView):
#    model = Accelerator
#    template_name = 'reviews/accelerator_detail.html'

# Testing old-style view for accelerator detail

def accelerator_detail(request, pk):
    accelerator = get_object_or_404(Accelerator, pk=pk)
    #reviews = Review.objects.all()
    context = {
        #'accelerator': accelerator,
        'reviews': reviews,
        #'reviews': Review.objects.filter(subject=accelerator.name).order_by('-date_posted')
    }
    return render(request, 'reviews/accelerator_detail.html', context)

# End test

class AcceleratorCreateView(LoginRequiredMixin, CreateView):
    model = Accelerator
    fields = ['name', 'summary', 'overall_rating'] # Need to remove overall_rating once a foreign key has been created

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AcceleratorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Accelerator
    fields = ['name', 'summary', 'overall_rating'] # Need to remove overall_rating once a foreign key has been created

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

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['subject', 'feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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