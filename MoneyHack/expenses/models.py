from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'Upi'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    way_of_payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='outgoing')

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.tag.name}"