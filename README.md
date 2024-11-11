# MoneyHack

MoneyHack is a comprehensive budget tracking solution designed to help you manage your finances effectively. It allows you to track your income and expenses, set and monitor goals, manage family budgets, and gain insights through analytics.

## Features

- **Chatbot**: Use the chatbot for easy navigation and instant help with your queries.
- **Expense Management**: Add, edit, and delete transactions. Import transactions from CSV files.
- **Goal Management**: Set and track individual and family goals.
- **Family Budget Management**: Manage your family budget by managing a family and tracking family goals.
- **Analytics**: Gain insights into your spending patterns with various charts and reports. Generate monthly reports.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/MoneyHack.git
    cd MoneyHack
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .myenv
    source .myenv/bin/activate  # On Windows use `.myenv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

6. Open your browser and go to `http://localhost:8000`.

## Usage

### Adding Transactions

1. Navigate to the "Expenses" page.
2. Click on "Add Transaction" and fill in the details.
3. Submit the form to add the transaction.

### Setting Goals

1. Navigate to the "Goals" page.
2. Click on "Add Goal" or "Add Family Goal" and fill in the details.
3. Submit the form to set the goal.

### Viewing Analytics

1. Navigate to the "Analytics" page.
2. View various charts and reports to gain insights into your spending patterns.

### Using the Chatbot

1. Navigate to the "Chatbot" page by cliking on the MoneyHack logo and then clicking the Chatbot icon.
2. Type your query in the input box and submit.
3. The chatbot will respond with the relevant information.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Plotly](https://plotly.com/)
- [Google Generative AI](https://ai.google/tools/)
