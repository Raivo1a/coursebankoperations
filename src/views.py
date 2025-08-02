import json

from src.utils import (date, total, top, get_data_time, filter_transactions_by_date, read_xlsx_file, currency_rates, stock_prices)


def main_info():
    '''Функция для главной страницы, объединяющая модуль utils'''

    user_input = input("Введите дату и время в формате YYYY-MM-DD HH:MM:SS ")
    transactions = read_xlsx_file('C:/Users/User/PycharmProjects/CourseBankOperations/data/operations.xlsx')
    greeting = date()
    cards = total(filter_transactions_by_date(transactions, user_input))
    top_transactions = top(filter_transactions_by_date(transactions, user_input))
    actual_currency_rates = [
        {"currency": "USD", "rate": currency_rates("USD")},
        {"currency": "EUR", "rate": currency_rates("EUR")},
    ]
    actual_stock_prices = [
        {"stock": "AAPL", "price": stock_prices("AAPL")},
        {"stock": "AMZN", "price": stock_prices("AMZN")},
        {"stock": "GOOGL", "price": stock_prices("GOOGL")},
        {"stock": "MSFT", "price": stock_prices("MSFT")},
        {"stock": "TSLA", "price": stock_prices("TSLA")},
        ]


    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": actual_currency_rates,
        "stock_prices": actual_stock_prices,
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
