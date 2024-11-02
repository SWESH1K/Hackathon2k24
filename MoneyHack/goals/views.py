from django.shortcuts import render, get_object_or_404, redirect
from .models import Goal
from .forms import GoalForm
from django.contrib.auth.decorators import login_required

@login_required
def goals(request):
    goals = Goal.objects.filter(user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            print('asdffdas')
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()
    return render(request, 'goals.html', {'goals': goals, 'form': form})

def edit_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_detail', pk=goal.pk)
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form})

def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if request.method == "POST":
        goal.delete()
        return redirect('goal_list')
    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})