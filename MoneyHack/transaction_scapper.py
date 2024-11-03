import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoneyHack.settings')
import django
django.setup()

import pandas as pd
from django.contrib.auth.models import User
from expenses.models import Transaction, Tag

class TransactionScapper():

    def __init__(self):
        self.data = None
        self.payment_method_mapping = {
            'CASH': 'Cash',
            'CREDIT CARD': 'Credit Card',
            'DEBIT CARD': 'Debit Card',
            'BANK TRANSFER': 'Bank Transfer',
            'UPI': 'UPI',
            'OTHER': 'Other'
        }
        self.csv_path = None

    def load_data(self, path: str):
        self.data = pd.read_excel(path, skiprows=20)

        # Drop rows where one or more columns contain only stars (*)
        self.data = self.data[~self.data.apply(lambda row: row.astype(str).str.fullmatch(r'\*+').any(), axis=1)]

        # Identify the first empty row and drop all rows from that row onwards
        first_empty_row_index = self.data[self.data.isnull().all(axis=1)].index
        if not first_empty_row_index.empty:
            self.data = self.data[:first_empty_row_index[0]]

        # Drop the last row
        self.data = self.data.iloc[:-1]

        # Classify transactions
        self.classify_transactions()

        print("Data loaded Successfully!")

    def classify_transactions(self):
        self.data['Narration'] = self.data['Narration'].astype(str)
        self.data['Payment Method'] = self.data['Narration'].apply(self.get_payment_method)
        self.data['Vendor'] = self.data['Narration'].apply(self.get_vendor_name)

    def get_payment_method(self, narration):
        for keyword, method in self.payment_method_mapping.items():
            if keyword in narration.upper():
                return method
        return 'Other'

    def get_vendor_name(self, narration):
        parts = narration.split('-')
        if len(parts) > 1:
            return parts[1].strip()
        return 'Unknown'

    def add_transactions_from_csv(self, csv_path: str):
        new_data = pd.read_csv(csv_path)
        new_data['Narration'] = new_data['Narration'].astype(str)
        new_data['Payment Method'] = new_data['Narration'].apply(self.get_payment_method)
        new_data['Vendor'] = new_data['Narration'].apply(self.get_vendor_name)
        self.data = pd.concat([self.data, new_data], ignore_index=True)
        print(f"Transactions from {csv_path} added Successfully!")

    def save_transactions_to_db(self, user_id: int):
        user = User.objects.get(id=user_id)
        # self.data = pd.read_csv('static/csv/new_data.csv')
        for _, row in self.data.iterrows():
            try:
                tag_name = row['Vendor']
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                amount = row['Withdrawal Amt.'] if not pd.isna(row['Withdrawal Amt.']) else row['Deposit Amt.']
                amount = amount if not pd.isna(amount) else 0  # Replace NaN with 0 or any default value
                # Ensure amount is a valid decimal number
                amount = float(amount)
                # Parse the date from the 'Date' column
                date = pd.to_datetime(row['Date'], format='%d/%m/%y')
                transaction = Transaction(
                    user=user,
                    amount=amount,
                    description=row['Vendor'],
                    tag=tag,
                    date=date,
                    way_of_payment=row['Payment Method'].lower().replace(' ', '_'),
                    transaction_type='outgoing' if not pd.isna(row['Withdrawal Amt.']) else 'incoming'
                )
                transaction.save()
            except ValueError:
                print(f"Skipping invalid transaction with narration: {row['Narration']}")
        print("Transactions saved to the database successfully!")

    def print_head(self):
        # Inspect the cleaned data
        print(self.data.head())

    def to_csv(self, path):
        self.data.to_csv(path)
        self.csv_path = path
        print(f"Data Successfully saved to - {path}")


def main():
    ts = TransactionScapper()
    ts.load_data('static/excel/Acct_Statement.xlsx')
    ts.print_head()
    ts.to_csv('static/csv/cleaned_transactions.csv')
    ts.save_transactions_to_db(user_id=1)

if __name__ == '__main__':
    main()