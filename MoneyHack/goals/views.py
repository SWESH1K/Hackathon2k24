from django.shortcuts import render, get_object_or_404, redirect
from .models import Goal, FamilyGoal
from expenses.models import Transaction
from .forms import GoalForm, FamilyGoalForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def goals(request):
    goals = Goal.objects.filter(user=request.user)
    family_goals = FamilyGoal.objects.filter(family__admins=request.user)

    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

    total_income = Transaction.objects.filter(
        user=request.user,
        date__gte=start_of_month,
        date__lte=end_of_month,
        transaction_type='incoming'
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Transaction.objects.filter(
        user=request.user,
        date__gte=start_of_month,
        date__lte=end_of_month,
        transaction_type='outgoing'
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_savings = total_income - total_expenses

    for goal in goals:
        months_remaining = (goal.due_date.year - now.year) * 12 + goal.due_date.month - now.month
        if months_remaining > 0:
            goal.monthly_target = goal.target_amount / months_remaining
        else:
            goal.monthly_target = goal.target_amount  # If due date is in the past or current month

    for family_goal in family_goals:
        months_remaining = (family_goal.due_date.year - now.year) * 12 + family_goal.due_date.month - now.month
        if months_remaining > 0:
            family_goal.monthly_target = family_goal.target_amount / months_remaining
        else:
            family_goal.monthly_target = family_goal.target_amount  # If due date is in the past or current month

    total_weightage = Goal.objects.filter(user=request.user).aggregate(total=Sum('weightage'))['total'] or 0

    if request.method == 'POST':
        if 'add_goal' in request.POST:
            form = GoalForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data.get('weightage') + total_weightage > 100:
                    messages.error(request, 'The total weightage of all goals cannot exceed 100%.')
                    return redirect('goals')
                goal = form.save(commit=False)
                goal.user = request.user
                goal.save()
                return redirect('goals')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error in {field}: {error}")
        elif 'add_family_goal' in request.POST:
            family_form = FamilyGoalForm(request.POST, request.FILES)
            if family_form.is_valid():
                family_goal = family_form.save(commit=False)
                try:
                    family_goal.family = request.user.family_admin.family
                except User.family_admin.RelatedObjectDoesNotExist:
                    messages.error(request, 'You are not an admin of any family.')
                    return redirect('goals')
                family_goal.save()
                return redirect('goals')
            else:
                for field, errors in family_form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error in {field}: {error}")
    else:
        form = GoalForm()
        family_form = FamilyGoalForm()

    return render(request, 'goals.html', {
        'goals': goals,
        'family_goals': family_goals,
        'form': form,
        'family_form': family_form,
        'current_savings': total_savings
    })

@login_required
def edit_goal(request, id):
    goal = get_object_or_404(Goal, id=id, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'edit_goal.html', {'form': form, 'goal': goal})

@login_required
def edit_family_goal(request, id):
    goal = get_object_or_404(Goal, id=id, user=request.user)
    if request.method == 'POST':
        form = FamilyGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals')
    else:
        form = FamilyGoalForm(instance=goal)
    return render(request, 'edit_family_goal.html', {'form': form, 'goal': goal})

@login_required
def delete_goal(request, id):
    goal = Goal.objects.get(id=id, user=request.user)
    goal.delete()
    return redirect('goals')

@login_required
def delete_family_goal(request):
    goal = FamilyGoal.objects.get(id=id, user=request.user)
    goal.delete()
    return redirect('goals')