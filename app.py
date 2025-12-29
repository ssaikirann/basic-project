import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from finance_tracker import (
    add_expense, add_investment, view_expenses, view_investments,
    get_total_expenses, get_total_investments, load_data, 
    EXPENSE_FILE, INVEST_FILE
)
from finance_tracker import get_supported_currencies, convert_amount

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Home route
@app.route('/')
def index():
    total_expenses = get_total_expenses()
    total_investments = get_total_investments()
    expenses = load_data(EXPENSE_FILE)
    investments = load_data(INVEST_FILE)
    
    return render_template('index.html',
                         total_expenses=total_expenses,
                         total_investments=total_investments,
                         expenses_count=len(expenses),
                         investments_count=len(investments))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    total_expenses = get_total_expenses()
    total_investments = get_total_investments()
    expenses = load_data(EXPENSE_FILE)
    investments = load_data(INVEST_FILE)
    
    # Category breakdown for expenses
    category_breakdown = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        category_breakdown[category] = category_breakdown.get(category, 0) + amount
    
    return render_template('dashboard.html',
                         total_expenses=total_expenses,
                         total_investments=total_investments,
                         expenses=expenses,
                         investments=investments,
                         category_breakdown=category_breakdown)

# Expenses routes
@app.route('/expenses')
def expenses():
    expenses = load_data(EXPENSE_FILE)
    return render_template('expenses.html', expenses=expenses)

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = load_data(EXPENSE_FILE)
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    try:
        expense = add_expense(
            data['category'],
            float(data['amount']),
            data.get('note', ''),
            data.get('currency', None)
        )
        return jsonify({'status': 'success', 'data': expense}), 201
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/expenses/<int:index>', methods=['PUT'])
def update_expense(index):
    data = request.get_json()
    expenses = load_data(EXPENSE_FILE)
    
    if 0 <= index < len(expenses):
        expenses[index].update({
            'category': data.get('category', expenses[index]['category']),
            'amount': float(data.get('amount', expenses[index]['amount'])),
            'note': data.get('note', expenses[index]['note'])
        })
        with open(EXPENSE_FILE, 'w') as f:
            json.dump(expenses, f, indent=4)
        return jsonify({'status': 'success', 'data': expenses[index]})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/api/expenses/<int:index>', methods=['DELETE'])
def delete_expense(index):
    expenses = load_data(EXPENSE_FILE)
    
    if 0 <= index < len(expenses):
        deleted = expenses.pop(index)
        with open(EXPENSE_FILE, 'w') as f:
            json.dump(expenses, f, indent=4)
        return jsonify({'status': 'success', 'message': 'Deleted'})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

# Investments routes
@app.route('/investments')
def investments():
    investments = load_data(INVEST_FILE)
    return render_template('investments.html', investments=investments)

@app.route('/api/investments', methods=['GET'])
def get_investments():
    investments = load_data(INVEST_FILE)
    return jsonify(investments)

@app.route('/api/investments', methods=['POST'])
def create_investment():
    data = request.get_json()
    try:
        investment = add_investment(
            data['type'],
            float(data['amount']),
            data.get('returns', ''),
            data.get('note', ''),
            data.get('currency', None)
        )
        return jsonify({'status': 'success', 'data': investment}), 201
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/investments/<int:index>', methods=['PUT'])
def update_investment(index):
    data = request.get_json()
    investments = load_data(INVEST_FILE)
    
    if 0 <= index < len(investments):
        investments[index].update({
            'type': data.get('type', investments[index]['type']),
            'amount': float(data.get('amount', investments[index]['amount'])),
            'returns': data.get('returns', investments[index]['returns']),
            'note': data.get('note', investments[index]['note'])
        })
        with open(INVEST_FILE, 'w') as f:
            json.dump(investments, f, indent=4)
        return jsonify({'status': 'success', 'data': investments[index]})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/api/investments/<int:index>', methods=['DELETE'])
def delete_investment(index):
    investments = load_data(INVEST_FILE)
    
    if 0 <= index < len(investments):
        deleted = investments.pop(index)
        with open(INVEST_FILE, 'w') as f:
            json.dump(investments, f, indent=4)
        return jsonify({'status': 'success', 'message': 'Deleted'})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

# Statistics API
@app.route('/api/stats')
def stats():
    expenses = load_data(EXPENSE_FILE)
    investments = load_data(INVEST_FILE)
    target_currency = request.args.get('target_currency', None)
    category_breakdown = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        category_breakdown[category] = category_breakdown.get(category, 0) + amount
    
    investment_types = {}
    for investment in investments:
        inv_type = investment['type']
        amount = investment['amount']
        investment_types[inv_type] = investment_types.get(inv_type, 0) + amount
    result = {
        'total_expenses': get_total_expenses(),
        'total_investments': get_total_investments(),
        'expense_count': len(expenses),
        'investment_count': len(investments),
        'category_breakdown': category_breakdown,
        'investment_types': investment_types
    }
    if target_currency:
        # attempt to provide converted totals
        try:
            tot_exp_conv = get_total_expenses(target_currency)
            tot_inv_conv = get_total_investments(target_currency)
            result['total_expenses_converted'] = tot_exp_conv
            result['total_investments_converted'] = tot_inv_conv
            result['converted_currency'] = target_currency.upper()
        except Exception:
            result['conversion_error'] = 'Conversion failed or unavailable'

    return jsonify(result)


@app.route('/api/currencies')
def currencies():
    symbols = get_supported_currencies()
    return jsonify({'symbols': symbols})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
