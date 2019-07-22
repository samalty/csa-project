from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
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
    #reviews = Review.objects.all()
    #print(accelerator)
    #print(len(reviews))
    context = {
        'accelerator': accelerator,
        'reviews': reviews,
    }
    return render(request, 'reviews/accelerator_detail.html', context)


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

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['subject', 'feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#def review_create(request):
#    review_form = RawReviewForm()
#    if request.method == 'POST':
#        review_form = RawReviewForm(request.POST)
#        if review_form.is_valid():
            #eview_form.save()
#            Review.objects.create(**review_form.cleaned_data)
#            return redirect(reviews)
#    context = {
#        'form': review_form
#    }
#    return render(request, 'reviews/review_form.html', context)


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