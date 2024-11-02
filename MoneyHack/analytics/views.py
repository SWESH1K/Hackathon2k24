from django.shortcuts import render
from expenses.models import Transaction
import plotly.express as px
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Get the current user's transactions
    transactions = Transaction.objects.filter(user=request.user)
    no_graphs = False
    if transactions.exists():
        # Create a DataFrame from the transactions
        data = {
            'Date': [transaction.date for transaction in transactions],
            'Tag': [transaction.tag.name for transaction in transactions],
            'Amount': [transaction.amount for transaction in transactions],
            'Type': [transaction.transaction_type for transaction in transactions],
            'Way of Payment': [transaction.way_of_payment for transaction in transactions],
        }
        df = pd.DataFrame(data)

        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Group by month and type, and sum the amounts
        df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
        df_grouped = df.groupby(['Month', 'Type']).agg({'Amount': 'sum'}).reset_index()
        df_grouped['Month'] = df_grouped['Month'].dt.to_pydatetime()
        df['Date'] = df['Date'].dt.date  # Convert to date


        # Group by tag and sum the amounts for the pie chart
        df_line = df.groupby(['Month', 'Tag']).agg({'Amount': 'sum'}).reset_index()
        df_pie = df[df['Type'] == 'outgoing'].groupby('Tag').agg({'Amount': 'sum'}).reset_index()
        df_top_expenses = df[df['Type'] == 'outgoing'].groupby('Tag').agg({'Amount': 'sum'}).reset_index()
        df_top_expenses = df_top_expenses.sort_values(by='Amount', ascending=False).head(5)
        df_credit_card = df[df['Way of Payment'] == 'credit_card'].groupby('Month').agg({'Amount': 'sum'}).reset_index()
        df_heatmap = df[df['Type'] == 'outgoing'].groupby('Date').agg({'Amount': 'sum'}).reset_index()
        df_heatmap['Date'] = pd.to_datetime(df_heatmap['Date'])
        df_heatmap['Day'] = df_heatmap['Date'].dt.day
        df_heatmap['Month'] = df_heatmap['Date'].dt.month_name()
        heatmap_data = df_heatmap.pivot(index='Day', columns='Month', values='Amount').fillna(0)

        # Create the plots
        fig_bar = px.bar(df_grouped, x='Month', y='Amount', color='Type', barmode='stack')
        fig_pie = px.pie(df_pie, names='Tag', values='Amount')
        fig_pie.update_traces(pull=[0.5 if i == 'hover' else 0 for i in df_pie['Tag']], hoverinfo='label+percent', textinfo='percent', textfont_size=20)
        fig_top_expenses = px.bar(
            df_top_expenses, 
            x='Amount', 
            y='Tag', 
            orientation='v', 
            labels={'Amount': 'Total Expense', 'Tag': 'Category'}
        )
        fig_top_expenses.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')), selector=dict(type='bar'))
        # Create the heatmap
        fig_heatmap = px.imshow(heatmap_data, 
                            labels=dict(x="Month", y="Day", color="Spending Amount"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index)
        fig_heatmap.update_traces(hoverinfo='x+y+z', selector=dict(type='heatmap'))
        fig_line = px.line(df_line, x='Month', y='Amount', color='Tag')
        fig_credit_card = px.line(df_credit_card, x='Month', y='Amount')
        fig_credit_card.update_traces(mode='lines+markers+text', textposition='top center', line=dict(color='darkblue'), marker=dict(color='red'))


        # Convert the plotly figures to HTML
        graph_bar = fig_bar.to_html(full_html=False)
        graph_pie = fig_pie.to_html(full_html=False)
        graph_top_expenses = fig_top_expenses.to_html(full_html=False)
        graph_heatmap = fig_heatmap.to_html(full_html=False)
        graph_line = fig_line.to_html(full_html=False)
        graph_credit_card = fig_credit_card.to_html(full_html=False)

        graphs={
            'graph_bar': graph_bar,
            'graph_pie': graph_pie,
            'graph_top_expenses': graph_top_expenses,
            'graph_line': graph_line,
            'graph_heatmap': graph_heatmap,
            'graph_credit_card': graph_credit_card,
        }
    
    else:
        no_graphs = True
        graphs = {}

    context = {
        'no_graphs': no_graphs,
        'graphs': graphs,
    }

    return render(request, 'analytics.html', context)