from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:measurement_id>/edit/', views.edit, name='edit'),
    path('<int:measurement_id>/delete/', views.delete, name='delete'),
]