from django.shortcuts import render
from expenses.models import Transaction
import plotly.express as px
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Get the current user's transactions
    transactions = Transaction.objects.filter(user=request.user)

    # Create a DataFrame from the transactions
    data = {
        'Date': [transaction.date for transaction in transactions],
        'Tag': [transaction.tag.name for transaction in transactions],
        'Amount': [transaction.amount for transaction in transactions],
        'Type': [transaction.transaction_type for transaction in transactions],
    }
    df = pd.DataFrame(data)

    # Group by month and type, and sum the amounts
    df['Month'] = df['Date'].dt.to_period('M')
    df_grouped = df.groupby(['Month', 'Type']).agg({'Amount': 'sum'}).reset_index()
    df_grouped['Month'] = df_grouped['Month'].dt.to_timestamp()

    # Create the stacked bar chart
    fig_bar = px.bar(df_grouped, x='Month', y='Amount', color='Type', barmode='stack', title='Monthly Inflows and Outflows')

    # Group by tag and sum the amounts for the pie chart
    df_pie = df[df['Type'] == 'outgoing'].groupby('Tag').agg({'Amount': 'sum'}).reset_index()

    # Create the pie chart
    fig_pie = px.pie(df_pie, names='Tag', values='Amount', title='Monthly Expense Breakdown')

    # Convert the plotly figures to HTML
    graph_bar = fig_bar.to_html(full_html=False)
    graph_pie = fig_pie.to_html(full_html=False)

    return render(request, 'analytics.html', {'graph_bar': graph_bar, 'graph_pie': graph_pie})