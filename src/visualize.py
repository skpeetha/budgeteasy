def plot_expense_pie(df, output_path=None):
    import matplotlib.pyplot as plt

    grouped = df.groupby('category')['withdrawal'].sum().dropna()
    if grouped.empty:
        return

    plt.figure(figsize=(6, 6))
    plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    if output_path:
        try:
            plt.savefig(output_path)
        except Exception as e:
            print(f"Error saving plot: {e}")
    else:
        plt.show()
    plt.close()
