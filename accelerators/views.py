from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from reviews.models import Accelerator, Review

class AcceleratorListView(ListView):
    model = Accelerator
    template_name = 'accelerators/accelerators_home.html'
    context_object_name = 'accelerators'
    ordering = ['-name']

def accelerator_detail(request, pk):
    accelerator = get_object_or_404(Accelerator, pk=pk)
    reviews = Review.objects.filter(subject=accelerator).order_by('-date_posted')[:4]
    context = {
        'accelerator': accelerator,
        'reviews': reviews,
    }
    print(accelerator.avg_mentorship)
    return render(request, 'accelerators/accelerator_detail.html', context)

def accelerator_reviews(request, pk):
    accelerator = get_object_or_404(Accelerator, pk=pk)
    reviews = Review.objects.filter(subject=accelerator).order_by('-date_posted')
    context = {
        'accelerator': accelerator,
        'reviews': reviews,
    }
    return render(request, 'accelerators/accelerator_reviews.html', context)

class AcceleratorCreateView(LoginRequiredMixin, CreateView):
    model = Accelerator
    template_name = 'accelerators/accelerator_form.html'
    fields = ['name', 'website', 'locations', 'bio', 'sector_focus', 'stage', 'deal', 'duration', 'logo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AcceleratorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Accelerator
    template_name = 'accelerators/accelerator_form.html'
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
    template_name = 'accelerators/accelerator_confirm_delete.html'
    success_url = "/accelerators/"
    
    def test_func(self):
        accelerator = self.get_object()
        if self.request.user == accelerator.author:
            return True
        return False