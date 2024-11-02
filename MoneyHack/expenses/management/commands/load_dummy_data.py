import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Transaction, Tag
from datetime import datetime

class Command(BaseCommand):
    help = 'Load dummy transactions from a CSV file'

    def handle(self, *args, **kwargs):
        with open('static/csv/user1_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = User.objects.get(id=row['user'])
                tag = Tag.objects.get(id=row['tag'])
                transaction = Transaction(
                    user=user,
                    amount=row['amount'],
                    description=row['description'],
                    tag=tag,
                    date=datetime.strptime(row['date'], '%Y-%m-%d'),  # Manually assign the date
                    way_of_payment=row['way_of_payment'],
                    transaction_type=row['transaction_type']
                )
                transaction.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added transaction: {transaction.description}'))