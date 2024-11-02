from django.shortcuts import render, redirect
from .models import Transaction, Tag
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user)
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('expenses')
    else:
        form = TransactionForm()
    return render(request, 'expenses.html', {'transactions': transactions, 'tags': tags, 'form': form})

@login_required
def edit_transaction(request, id):
    transaction = Transaction.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id, user=request.user)
    transaction.delete()
    return redirect('expenses')