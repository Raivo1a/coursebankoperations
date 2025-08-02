from src.reports import categories
from src.services import process_bank_search
from src.utils import read_xlsx_file
from src.views import main_info


def main():
    """Главная функция, запускающая все"""
    print(main_info())  # вывод главной страницы

    transactions = read_xlsx_file("C:/Users/User/PycharmProjects/CourseBankOperations/data/operations.xlsx")
    user_search = input("Введите слово для поиска ")
    print(process_bank_search(transactions, user_search))  # вывод простого поиска

    user_category = input("Введите категорию: ")
    user_start_date = input("Введите дату начала поиска (период поиска - 3 месяца, формат ввода YYYY-MM-DD): ")
    print(categories(user_category, user_start_date))  # вывод трат по категориям
    print(f'Траты по категории {user_category} выведены в файл')

if __name__ == "__main__":
    print(main())
