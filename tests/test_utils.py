import datetime
from unittest.mock import patch

import pytest

from src.utils import date, get_data_time, read_xlsx_file, top, total


@patch("pandas.read_excel")
def test_read_xlsx_file(mock_read_xlsx):
    mock_read_xlsx.return_value.to_dict.return_value = [
        {"test_dict": "01", "test_key": "test_value_1"},
        {"test_dict": "02", "test_key": "test_value_2"},
    ]
    assert read_xlsx_file("test_file_path.xlsx") == [
        {"test_dict": "01", "test_key": "test_value_1"},
        {"test_dict": "02", "test_key": "test_value_2"},
    ]


def test_date():
    morning_time = datetime.datetime(2023, 1, 1, 6)
    assert date(morning_time) == "Доброе утро"

    afternoon_time = datetime.datetime(2023, 1, 1, 14)
    assert date(afternoon_time) == "Добрый день"

    evening_time = datetime.datetime(2023, 1, 1, 20)
    assert date(evening_time) == "Добрый вечер"

    night_time = datetime.datetime(2023, 1, 1, 23)
    assert date(night_time) == "Добрый ночи"


@pytest.mark.parametrize(
    "date, date_format, expected_result",
    [
        ("2023-01-15 10:30:00", "%Y-%m-%d %H:%M:%S", ["2023-01-01 10:30:00", "2023-01-15 10:30:00"]),
        ("2024-02-01 00:00:00", "%Y-%m-%d %H:%M:%S", ["2024-02-01 00:00:00", "2024-02-01 00:00:00"]),
        ("2023-03-31 23:59:59", "%Y-%m-%d %H:%M:%S", ["2023-03-01 23:59:59", "2023-03-31 23:59:59"]),
    ],
)
def test_get_data_time(date, date_format, expected_result):
    result = get_data_time(date, date_format)
    assert result == expected_result


def test_total(transactions_fixture):
    expected = [
        {"cashback": 1.63, "last_digits": "7197", "total_spent": 163.0},
        {"cashback": 11.14, "last_digits": "5133", "total_spent": 1114.2},
        {"cashback": 2.5, "last_digits": "4556", "total_spent": 250.0},
    ]
    assert total(transactions_fixture) == expected


def test_top(transactions_fixture):
    expected = [
        {"amount": -69.0, "category": "Топливо", "date": "16.01.2018", "description": "Shell"},
        {"amount": -94.0, "category": "Транспорт", "date": "13.01.2018", "description": "Яндекс Такси"},
        {"amount": -124.9, "category": "Фастфуд", "date": "20.01.2018", "description": "Бургер Кинг"},
        {"amount": -149.0, "category": "Сервис", "date": "18.01.2018", "description": "Avito"},
        {"amount": -250.0, "category": "Связь", "date": "10.01.2018", "description": "МТС"},
    ]
    assert top(transactions_fixture) == expected
