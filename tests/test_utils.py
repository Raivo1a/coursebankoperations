import pytest
from unittest.mock import patch

from src.utils import read_xlsx_file, date, total, top


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


@pytest.mark.parametrize(
    "_input, _output",
    [
        ("2018-01-01 14:20:30", "Добрый день!"),
        ("2018-01-01 07:02:33", "Доброе утро!"),
        ("2018-01-01 18:05:13", "Добрый вечер!"),
        ("2018-01-01 01:05:05", "Доброй ночи!"),
    ],
)
def test_date(_input: str, _output: str) -> None:
    assert date(_input) == _output


def test_total(transactions_fixture):
    expected = [
        {
            "last_digits": 7197,
            "total_spent": 163,
            "cashback": 1.63
        }
    ]
    assert total(transactions_fixture) == expected


def test_top(transactions_fixture):
    expected = [
        {
            "date": "14.01.2018",
            "amount": -69.0,
            "category": "Топливо",
            "description": "Shell"
        },
        {
            "date": "11.01.2018",
            "amount": -94.0,
            "category": "Транспорт",
            "description": "Яндекс Такси"
        },
        {
            "date": "18.01.2018",
            "amount": -124.9,
            "category": "Фастфуд",
            "description": "Бургер Кинг"
        },
        {
            "date": "16.01.2018",
            "amount": -149.0,
            "category": "Сервис",
            "description": "Avito"
        },
        {
            "date": "08.01.2018",
            "amount": -250.0,
            "category": "Связь",
            "description": "МТС"
        }
    ]
    assert top(transactions_fixture) == expected
