from django.urls import path
from . import views

urlpatterns = [
    path('', views.goals, name='goals'),
    path('add/', views.goals, name='add_goal'),
    path('edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('delete/<int:id>/', views.delete_goal, name='delete_goal'),
    path('edit_family_goal/<int:id>/', views.edit_family_goal, name='edit_family_goal'),
    path('delete_family_goal/<int:id>/', views.delete_family_goal, name='delete_family_goal'),
]