import re
def categorize_transactions(row):
    desc = str(row['description']).lower()
    deposit = row.get('deposit')
    withdrawal = row.get('withdrawal')

    # Rule 1: Self transfer or refund
    if 'refund' in desc or 'reverse' in desc:
        return 'Refund / Reversal'
    if re.search(r'@\w+.*@\w+', desc):  # repeated UPI ID
        upis = re.findall(r'@\w+', desc)
        if len(upis) >= 2 and upis[0] == upis[1]:
            return 'Self Transfer'

    # Rule 2: Payments to services
    service_keywords = ['cred', 'lazypay', 'rentomojo', 'swiggy', 'zomato', 'amazon', 'flipkart']
    if any(keyword in desc for keyword in service_keywords):
        return 'Service Payment'

    # Rule 3: Utilities / subscriptions
    utility_keywords = ['electricity', 'broadband', 'recharge', 'netflix', 'billdesk']
    if any(keyword in desc for keyword in utility_keywords):
        return 'Utility / Subscription'

    # Rule 4: P2P transfers
    if re.search(r'@\w+', desc) and any(word in desc for word in ['phonepe', 'ybl', 'paytm']):
        return 'P2P Transfer'

    # Rule 5: Cash operations
    if 'atm' in desc or 'cash' in desc or 'withdraw' in desc:
        return 'Cash'

    # Rule 6: Salary or major inflows
    try:
        if deposit and float(str(deposit).replace(',', '')) > 20000:
            return 'Income / Salary'
    except:
        pass

    # Default
    return 'Other'
