from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Tag
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from transaction_scapper import TransactionScapper
from .forms import TransactionForm, UploadFileForm

@login_required
def upload_transactions(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            ts = TransactionScapper()
            ts.load_data(file)
            ts.print_head()
            ts.to_csv('static/csv/cleaned_transactions.csv')
            ts.save_transactions_to_db(user_id=request.user.id)
            return redirect('expenses')
    else:
        form = UploadFileForm()
    return render(request, 'upload_transactions.html', {'form': form})

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user)
    tags = Tag.objects.all()

    # Calculate totals
    total_incoming = transactions.filter(transaction_type='incoming').aggregate(total=Sum('amount'))['total'] or 0
    total_outgoing = transactions.filter(transaction_type='outgoing').aggregate(total=Sum('amount'))['total'] or 0
    total_savings = total_incoming - total_outgoing

    # Calculate current month totals
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_incoming = transactions.filter(transaction_type='incoming', date__gte=start_of_month).aggregate(total=Sum('amount'))['total'] or 0
    current_month_outgoing = transactions.filter(transaction_type='outgoing', date__gte=start_of_month).aggregate(total=Sum('amount'))['total'] or 0
    current_month_savings = current_month_incoming - current_month_outgoing

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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = TransactionForm()

    return render(request, 'expenses.html', {
        'transactions': transactions,
        'tags': tags,
        'form': form,
        'total_incoming': total_incoming,
        'total_outgoing': total_outgoing,
        'total_savings': total_savings,
        'current_month_incoming': current_month_incoming,
        'current_month_outgoing': current_month_outgoing,
        'current_month_savings': current_month_savings,
    })

@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = TransactionForm(instance=transaction)
    tags = Tag.objects.all()
    return render(request, 'edit_transaction.html', {'form': form, 'transaction': transaction, 'tags': tags})

@login_required
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id, user=request.user)
    transaction.delete()
    return redirect('expenses')

@login_required
def budget_report(request):
    return render(request, 'budget_report.html')

import calendar

@login_required
def generate_report(request):
    if request.method == 'POST':
        report_month = request.POST.get('report_month')
        year, month = map(int, report_month.split('-'))
        start_date = timezone.datetime(year, month, 1)
        end_date = timezone.datetime(year, month, calendar.monthrange(year, month)[1])

        transactions = Transaction.objects.filter(user=request.user, date__range=[start_date, end_date])
        total_income = transactions.filter(transaction_type='incoming').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = transactions.filter(transaction_type='outgoing').aggregate(total=Sum('amount'))['total'] or 0
        total_savings = total_income - total_expenses

        context = {
            'report_month': calendar.month_name[month],
            'report_year': year,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'transactions': transactions,
        }
        return render(request, 'budget_report.html', context)
    return redirect('expenses')