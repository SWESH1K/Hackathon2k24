from django.shortcuts import render, get_object_or_404, redirect
from .models import Goal
from expenses.models import Transaction
from .forms import GoalForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.contrib import messages

@login_required
def goals(request):
    goals = Goal.objects.filter(user=request.user)
    
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

    print(start_of_month, end_of_month)
    print(total_income, total_expenses, total_savings)

    total_weightage = Goal.objects.filter(user=request.user).aggregate(total=Sum('weightage'))['total'] or 0
    print("total:",total_weightage)
    if request.method == 'POST':
        form = GoalForm(request.POST, request.FILES)
        print("error2")
        if form.is_valid():
            if form.cleaned_data.get('weightage') + total_weightage > 100:
                print("The total weightage of all goals cannot exceed 100%.")
                messages.error(request, 'The total weightage of all goals cannot exceed 100%.')
                return redirect('goals')
            goal = form.save(commit=False)
            goal.user = request.user
            print(form.cleaned_data.get('icon'))
            goal.save()
            return redirect('goals')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = GoalForm()
    return render(request, 'goals.html', {'goals': goals, 'form': form, 'current_savings': total_savings})

def edit_goal(request, id):
    goal = Goal.objects.get(id=id, user=request.user)
    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals', id=goal.id)
    else:
        form = GoalForm(instance=goal)
    return render(request, 'edit_goal.html', {'form': form})

def delete_goal(request, id):
    goal = Goal.objects.get(id=id, user=request.user)
    goal.delete()
    return redirect('goals')