from django.urls import path
from . import views

urlpatterns = [
    path('', views.family, name='family'),
    path('create/', views.create_family, name='create_family'),
    path('invite/<username>', views.invite_member, name='invite_member'),
    path('leave/', views.leave_family, name='leave_family'),
    path('add_members/', views.add_members, name='add_members'),
    path('accept_invitation/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),  # Add this line
    path('decline_invitation/<int:invitation_id>/', views.decline_invitation, name='decline_invitation'),  # Add this line
]