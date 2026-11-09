# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template('transactions.html', transactions=transactions) # This is so transactions.html knows what data to load.

# Create operation: Display add transaction form
# Route to handle the creation of a new transaction
@app.route("/add", methods=['GET', 'POST'])
def add_transaction():
    # If the request method is GET, render the form template to display the add transaction form
    if request.method == 'GET':
        return render_template('form.html')
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,                # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],               # Get the 'date' field value from the form
            'amount': float(request.form['amount'])     # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)
        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for('get_transactions'))

# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    if request.method == 'GET':
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                # Render the edit form template and pass the transaction to be edited
                return render_template("edit.html", transaction=transaction)
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
         # Extract the updated values from the form fields
        date = request.form['date']             # Get the 'date' field value from the form
        amount = float(request.form['amount'])  # Get the 'amount' field value from the form and convert it to a float

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))

# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
            if transaction['id'] == transaction_id:
                transactions.remove(transaction)    # Remove the transaction from the transactions list
                break                               # Exit the loop once the transaction is found and removed
    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# Search function
@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        minimum = float(request.form['min_amount'])
        maximum = float(request.form['max_amount'])
        filtered_transactions = [transaction for transaction in transactions if transaction['amount'] >= minimum and transaction['amount'] <= maximum]
        return render_template("transactions.html", transactions=filtered_transactions)
    if request.method == 'GET':
        return render_template("search.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

