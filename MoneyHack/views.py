from django.shortcuts import render, redirect
from .models import Transaction, Tag
from django.contrib.auth.decorators import login_required

@login_required
def expenses(request):
    transactions = Transaction.objects.filter(user=request.user)
    tags = Tag.objects.all()
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        tag_id = request.POST['tag']
        tag = Tag.objects.get(id=tag_id)
        Transaction.objects.create(user=request.user, amount=amount, description=description, tag=tag)
        return redirect('expenses')
    return render(request, 'expenses.html', {'transactions': transactions, 'tags': tags})
