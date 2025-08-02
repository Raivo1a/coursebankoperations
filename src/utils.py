import logging

import pandas as pd
from datetime import datetime, timedelta
import os
import yfinance as yf

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("C:/Users/User/PycharmProjects/CourseBankOperations/logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_xlsx_file(path: str) -> list:
    """Обрабатывает XLSX-файл и преобразует в список транзакций"""
    logger.info("Запрос на преобразование файла xlsx")
    try:
        logger.info("Список транзакций успешно создан")
        df = pd.read_excel(path)
        result = df.to_dict(orient="records")
        return result
    except FileNotFoundError:
        logger.error("Ошибка! Файл не найден")
        return []
    except Exception:
        logger.error("Ошибка! Файл пуст")
        return []


def date():
    '''Обрабатывает текущую дату и возвращает приветствие'''
    current_date_time = datetime.now()
    hour = current_date_time.hour
    if 5 <= hour < 12:
        return 'Доброе утро'
    elif 12 <= hour < 18:
        return 'Добрый день'
    elif 18 <= hour < 22:
        return 'Добрый вечер'
    else:
        return 'Добрый ночи'


def get_data_time(user_date: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    '''Обрабатывает текущую дату и возвращает дату начала месяца'''
    date_time = datetime.strptime(user_date, date_format)
    start_of_month = date_time.replace(day=1)
    return [
        start_of_month.strftime("%Y-%m-%d %H:%M:%S"),
        date_time.strftime("%Y-%m-%d %H:%M:%S")
        ]


transactions = read_xlsx_file('C:/Users/User/PycharmProjects/CourseBankOperations/data/operations.xlsx')

def filter_transactions_by_date(transactions: list, user_dates: str):
    '''Функция фильтрует список транзакций на период с первого числа по введенное пользователем'''
    start_date, end_date = get_data_time(user_dates)
    df_transactions = pd.DataFrame(transactions)
    df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'], dayfirst=True)
    filtered_df = df_transactions[
        (df_transactions['Дата операции'] >= start_date) &
        (df_transactions['Дата операции'] <= end_date)
    ]
    return filtered_df.to_dict(orient="records")


def total(filtered):
    '''Функция возвращает 4 последние цифры номера карты из excel файла, считает общую сумму трат и кэшбек по каждой карте'''
    card_totals = {}
    card_total = []
    for transaction in filtered:
        card_number_raw = transaction.get("Номер карты")
        amount_raw = transaction.get("Сумма операции")
        if card_number_raw is None:
            continue
        card_number = str(card_number_raw)
        if amount_raw is None:
            continue
        spent = float(amount_raw)
        if spent < 0:
            spent = abs(spent)
            card_number = card_number[1:]
            if card_number != "an":
                current_total = card_totals.get(card_number, 0.0)
                new_total = current_total + spent
                card_totals[card_number] = round(new_total, 2)
    for card_number, total_spent in card_totals.items():
        cashback = round(card_totals[card_number] / 100, 2)
        card_total.append({"last_digits": card_number,
                            "total_spent": total_spent,
                            "cashback": cashback})
    return card_total


def top(filtered):
    '''Функция показывает топ 5 транзакций по карте'''
    top_transactions = []
    for transaction in filtered:
        date = transaction.get("Дата платежа")
        amount = transaction.get("Сумма операции")
        category = transaction.get("Категория")
        description = transaction.get("Описание")
        if amount is None or date is None:
            continue
        top_transactions.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        })
    top_transactions.sort(key=lambda x: x["amount"], reverse=True)
    return top_transactions[:5]


def currency_rates(currency: str):
    '''Функция показывает курс валют'''
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
    headers = {"apikey": os.getenv("APILAYER_KEY")}
    response = requests.get(url, headers=headers)
    rates = round(response.json()["result"], 2)
    return rates


def stock_prices(stock: str):
    '''Функция показывает стоимость акций'''
    stock_data = yf.Ticker(stock)
    todays_data = stock_data.history(period="1d")
    return round(todays_data["High"].iloc[0], 2)
