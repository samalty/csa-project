from django.urls import path
from .views import (
    ReviewListView,
    ReviewDetailView,
    review_create,
    review_update,
    review_delete,
)
from . import views

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/new/', views.review_create, name='review_post'),
    path('<int:pk>/edit/', views.review_update, name='review_edit'),
    path('<int:pk>/delete/', views.review_delete, name='review_delete'),
]