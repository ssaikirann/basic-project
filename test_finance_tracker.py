import pytest
import json
import os
from finance_tracker import (
    add_expense,
    add_investment,
    view_expenses,
    view_investments,
    get_total_expenses,
    get_total_investments,
    load_data,
    save_data,
    EXPENSE_FILE,
    INVEST_FILE
)


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test files before and after tests"""
    for file in [EXPENSE_FILE, INVEST_FILE]:
        if os.path.exists(file):
            os.remove(file)
    yield
    for file in [EXPENSE_FILE, INVEST_FILE]:
        if os.path.exists(file):
            os.remove(file)


class TestExpenses:
    def test_add_expense(self):
        expense = add_expense("food", 50.0, "lunch")
        assert expense["category"] == "food"
        assert expense["amount"] == 50.0
        assert expense["note"] == "lunch"

    def test_add_multiple_expenses(self):
        add_expense("food", 50.0, "lunch")
        add_expense("rent", 1000.0, "monthly rent")
        add_expense("travel", 100.0, "taxi")

        total = get_total_expenses()
        assert total == 1150.0

    def test_get_total_expenses_empty(self):
        total = get_total_expenses()
        assert total == 0

    def test_view_expenses_empty(self):
        result = view_expenses()
        assert "No expenses recorded yet" in result

    def test_view_expenses_with_data(self):
        add_expense("food", 50.0, "lunch")
        result = view_expenses()
        assert "food" in result
        assert "50.0" in result
        assert "lunch" in result
        assert "Total Spent: 50.0" in result


class TestInvestments:
    def test_add_investment(self):
        investment = add_investment("stocks", 1000.0, "10%", "tech stocks")
        assert investment["type"] == "stocks"
        assert investment["amount"] == 1000.0
        assert investment["returns"] == "10%"
        assert investment["note"] == "tech stocks"

    def test_add_multiple_investments(self):
        add_investment("stocks", 1000.0, "10%", "tech stocks")
        add_investment("crypto", 500.0, "20%", "bitcoin")
        add_investment("mutual fund", 2000.0, "8%", "index fund")

        total = get_total_investments()
        assert total == 3500.0

    def test_get_total_investments_empty(self):
        total = get_total_investments()
        assert total == 0

    def test_view_investments_empty(self):
        result = view_investments()
        assert "No investments recorded yet" in result

    def test_view_investments_with_data(self):
        add_investment("stocks", 1000.0, "10%", "tech stocks")
        result = view_investments()
        assert "stocks" in result
        assert "1000.0" in result
        assert "10%" in result
        assert "Total Invested: 1000.0" in result


class TestDataManagement:
    def test_save_and_load_data(self):
        data = [{"name": "test", "value": 100}]
        test_file = "test_data.json"
        
        save_data(test_file, data)
        loaded_data = load_data(test_file)
        
        assert loaded_data == data
        
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_load_nonexistent_file(self):
        result = load_data("nonexistent.json")
        assert result == []

    def test_expense_amount_validation(self):
        with pytest.raises(ValueError):
            add_expense("food", -50, "invalid")

    def test_investment_amount_validation(self):
        with pytest.raises(ValueError):
            add_investment("stocks", -100, "10%", "invalid")
