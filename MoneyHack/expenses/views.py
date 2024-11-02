from django.shortcuts import render, redirect
from .models import Transaction, Tag
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user)
    tags = Tag.objects.all()

    # Apply filters
    tag_id = request.GET.get('tag')
    month = request.GET.get('month')
    search = request.GET.get('search')
    way_of_payment = request.GET.get('way_of_payment')

    if tag_id:
        transactions = transactions.filter(tag_id=tag_id)
    if month:
        year, month = map(int, month.split('-'))
        transactions = transactions.filter(date__year=year, date__month=month)
    if search:
        transactions = transactions.filter(description__icontains=search)
    if way_of_payment:
        transactions = transactions.filter(way_of_payment=way_of_payment)

    # Show only the last 20 transactions by default
    transactions = transactions.order_by('-date')[:20]

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