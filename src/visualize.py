# visualize.py

import matplotlib.pyplot as plt

def plot_expense_pie(df):
    # Filter only expenses
    expense_df = df[df['withdrawal'].notnull()].copy()

    # Group by category and sum expenses
    category_totals = expense_df.groupby('category')['withdrawal'].sum()

    # Plot pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=140)
    plt.title('Spending by Category')
    plt.axis('equal')  # Equal aspect ratio ensures pie is circular
    plt.tight_layout()
    plt.savefig('plot.png')
    plt.show()
