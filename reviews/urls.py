from django.urls import path
from .views import (
    AcceleratorListView, 
    accelerator_detail,
    #AcceleratorDetailView, 
    AcceleratorCreateView, 
    AcceleratorUpdateView, 
    AcceleratorDeleteView,
    ReviewListView,
    ReviewDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
)
from . import views

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    #path('new/', views.review_create, name='review_create'),
    path('new/', ReviewCreateView.as_view(), name="review_create"),
    path('<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('accelerators/', AcceleratorListView.as_view(), name='accelerators'),
    path('accelerator/<int:pk>/', views.accelerator_detail, name='accelerator_detail'),
    #path('accelerator/<int:pk>/', AcceleratorDetailView.as_view(), name='accelerator_detail'),
    path('accelerator/new/', AcceleratorCreateView.as_view(), name='accelerator_create'),
    path('accelerator/<int:pk>/update/', AcceleratorUpdateView.as_view(), name='accelerator_update'),
    path('accelerator/<int:pk>/delete/', AcceleratorDeleteView.as_view(), name='accelerator_delete'),
]