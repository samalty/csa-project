from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def reviews(request):
    return render(request, 'reviews/reviews-home.html')

@login_required
def add_review(request):
    return render(request, 'reviews/add-review.html')