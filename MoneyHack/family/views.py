from django.shortcuts import render, redirect, get_object_or_404
from .models import Family, Invitation, FamilyMember, FamilyAdmin
from .forms import FamilyGroupForm, InviteMemberForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def family(request):
    user_families = request.user.member_of_family.all() | request.user.admin_of_family.all()
    pending_invitations = Invitation.objects.filter(receiver=request.user)
    return render(request, 'family.html', {'user_families': user_families, 'pending_invitations': pending_invitations})

@login_required
def create_family(request):
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        if family_name:
            family = Family.objects.create(name=family_name)
            family.admins.add(request.user)
            family.save()  # Save the family object to get an ID
            members_usernames = request.POST.get('members', '').split(',')
            for username in members_usernames:
                username = username.strip()
                if username:
                    try:
                        user = User.objects.get(username=username)
                        Invitation.objects.create(family=family, receiver=user, sender=request.user)
                        messages.success(request, f'Invitation sent to {username}.')
                    except User.DoesNotExist:
                        messages.error(request, f'User {username} does not exist.')
            messages.success(request, 'Family group created successfully.')
            return redirect('family')
        else:
            messages.error(request, 'Family name is required.')
    return redirect('family')

@login_required
def invite_member(request):
    if request.method == 'POST':
        form = InviteMemberForm(request.POST)
        if form.is_valid():
            usernames = form.cleaned_data['usernames'].split(',')
            for username in usernames:
                username = username.strip()
                if username:
                    try:
                        user = User.objects.get(username=username)
                        Invitation.objects.create(family=request.user.family_member.family, receiver=user, sender=request.user)
                        messages.success(request, f'Invitation sent to {username}.')
                    except User.DoesNotExist:
                        messages.error(request, f'User {username} does not exist.')
            return redirect('family')
    else:
        form = InviteMemberForm()
    return render(request, 'invite_member.html', {'form': form})

@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, receiver=request.user)
    invitation.save()
    invitation.family.members.add(request.user)
    messages.success(request, 'You have joined the family.')
    return redirect('family')

@login_required
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, receiver=request.user)
    invitation.status = 'declined'
    invitation.save()
    messages.success(request, 'You have declined the invitation.')
    return redirect('family')

@login_required
def leave_family(request):
    try:
        family_member = request.user.family_member
        family = family_member.family
        family.members.remove(request.user)
        family_member.delete()
    except FamilyMember.DoesNotExist:
        try:
            family_admin = request.user.family_admin
            family = family_admin.family
            family.admins.remove(request.user)
            family_admin.delete()
        except FamilyAdmin.DoesNotExist:
            messages.error(request, 'You are not a member or admin of any family.')
            return redirect('family')
    messages.success(request, 'You have left the family.')
    return redirect('family')

from django.contrib.auth.models import User

@login_required
def add_members(request):
    if request.method == 'POST':
        invitees = request.POST.getlist('invitees')
        family = request.user.family_admin.family
        for username in invitees:
            try:
                user = User.objects.get(username=username)
                Invitation.objects.create(family=family, receiver=user, sender=request.user)
                messages.success(request, f'Invitation sent to {username}.')
            except User.DoesNotExist:
                messages.error(request, f'User {username} does not exist.')
        return redirect('family')
    else:
        # Exclude users who are already members or admins of any family
        users = User.objects.exclude(
            family_member__isnull=False
        ).exclude(
            family_admin__isnull=False
        )
        return render(request, 'add_members.html', {'users': users})

@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, receiver=request.user)
    invitation.family.members.add(request.user)
    invitation.delete()
    messages.success(request, 'You have joined the family.')
    return redirect('family')

@login_required
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, receiver=request.user)
    invitation.delete()
    messages.success(request, 'You have declined the invitation.')
    return redirect('family')