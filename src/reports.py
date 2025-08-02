import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import json
import logging


logger = logging.getLogger("reports")
file_handler = logging.FileHandler("C:/Users/User/PycharmProjects/CourseBankOperations/logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


transactions_df = pd.read_excel('C:/Users/User/PycharmProjects/CourseBankOperations/data/operations.xlsx')


def report_to_file(filename: str = "report.xlsx") -> callable:
    def decorator(func):
        def wrapper(*args, **kwargs):
            result: pd.DataFrame = func(*args, **kwargs)
            result.to_excel(filename)
            return result

        return wrapper

    return decorator


@report_to_file()
def spent_by_category(transactions_df: pd.DataFrame, category: str, start_date: Optional[str] = None) -> pd.DataFrame:
    '''Функция показывает траты по категориям'''
    logger.info("Запрос на поиск")
    if start_date is None:
        start_date_df = datetime.now()
    else:
        start_date_df = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_df = start_date_df + timedelta(days=90)
    transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'], dayfirst=True)
    filtered_transactions = transactions_df[
        (transactions_df['Категория'] == category)
        & (transactions_df['Дата операции'] >= start_date_df)
        & (transactions_df['Дата операции'] < end_date_df)
    ]
    logger.info("Поиск успешно выполнен")
    return filtered_transactions


def categories(category, start_date):
    '''Функция записывает spent_by_category в json файл'''
    filtered_operations_df = spent_by_category(transactions_df, category, start_date)

    data_to_save = filtered_operations_df.to_dict("records")
    for record in data_to_save:
        for key, value in record.items():
            if isinstance(value, pd.Timestamp):
                record[key] = value.isoformat()

    with open('reports.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)
