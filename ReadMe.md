# MoneyHack

MoneyHack is your ultimate budget tracking solution. It helps you manage your finances by tracking your income and expenses, setting budgets, and providing insightful reports.

## Features

1. **User Registration and Login**
   - **Register**: Create a new account by providing a username, password, and email.
   - **Login**: Log in using your username and password.
   - **Logout**: Log out of your account.

2. **Profile Management**
   - **View Profile**: View your profile information, including your username and email.
   - **Update Profile**: Update your salary and budget information from your profile page.

3. **Expense Management**
   - **Add Transaction**: Add a new transaction with details such as amount, description, and tag.
   - **View Transactions**: View all your transactions in a table format.
   - **Edit Transaction**: Edit existing transactions.
   - **Delete Transaction**: Delete transactions you no longer need.
   - **Filter Transactions**: Filter transactions based on tags and date (month).

4. **Analytics**
   - **Generate Reports**: Generate detailed reports to analyze your financial health and make informed decisions.

5. **Family Management**
   - **Add Family Members**: Add users as family members or admins.
   - **Remove Family Members**: Remove users from the family.
   - **View Family Members**: View all family members and their roles.

6. **AI ChatBot**
   - **ChatBot Integration**: Interact with an AI ChatBot to get assistance with managing your finances and using the application.

## Instructions to Clone and Run the Project

### Prerequisites

- Python 3.11.9
- Django 5.1.2
- Virtual Environment (recommended)

### Clone the Repository

```sh
git clone https://github.com/SWESH1K/MoneyHack.git
cd MoneyHack
```

### Set Up the Virtual Environment

```sh
python -m venv .myenv
source .myenv/Scripts/activate  # On Windows
source .myenv/bin/activate      # On macOS/Linux
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Set Up the Database

```sh
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server

```sh
python manage.py runserver
```

## Acknowledgements

This project was made by team number IMPHAC24TM07 in the Hack-A-Thon 2k24.