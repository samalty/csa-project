from django.urls import path
from .views import (
    AcceleratorListView, 
    accelerator_detail,
    accelerator_reviews,
    AcceleratorCreateView, 
    AcceleratorUpdateView, 
    AcceleratorDeleteView,
)
from . import views

urlpatterns = [
    path('', AcceleratorListView.as_view(), name='accelerators'),
    path('<int:pk>/', views.accelerator_detail, name='accelerator_detail'),
    path('new/', AcceleratorCreateView.as_view(), name='accelerator_create'),
    path('<int:pk>/update/', AcceleratorUpdateView.as_view(), name='accelerator_update'),
    path('<int:pk>/delete/', AcceleratorDeleteView.as_view(), name='accelerator_delete'),
    path('<int:pk>/reviews/', views.accelerator_reviews, name='accelerator_reviews'),
]