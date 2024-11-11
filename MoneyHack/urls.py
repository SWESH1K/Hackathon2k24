from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expenses, name='expenses'),
    # ... other URL patterns ...
]
