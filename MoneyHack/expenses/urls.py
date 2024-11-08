# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='expenses'),
    path('add/', views.home, name='add_transaction'),
    path('edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('upload/', views.upload_transactions, name='upload_transactions'),  # Added URL for uploading transactions
    # Todo: remove this path
    path('budget_report/', views.generate_report, name='generate_report')
]