from datetime import datetime

import pandas as pd

from src.reports import spent_by_category


def test_spent_by_category(transactions_fixture_df):
    category = "Еда"
    start_date_str = "2023-01-01"
    expected_data = {
        "Дата операции": [
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 15, 11, 0),
            datetime(2023, 1, 25, 12, 0),
        ],
        "Категория": ["Еда", "Еда", "Еда"],
        "Сумма": [-100.5, -250.75, -150.0],
    }
    expected_df = pd.DataFrame(expected_data)
    result_df = spent_by_category(transactions_fixture_df, category, start_date_str)
    pd.testing.assert_frame_equal(result_df, expected_df)
