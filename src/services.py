import json
import logging
import re

from src.utils import read_xlsx_file

logger = logging.getLogger("services")
file_handler = logging.FileHandler(
    "C:/Users/User/PycharmProjects/CourseBankOperations/logs/services.log", "w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


transactions = read_xlsx_file("C:/Users/User/PycharmProjects/CourseBankOperations/data/operations.xlsx")


def process_bank_search(data: list[dict], search: str):
    """Поиск в списке операций по заданной строке. Возвращает список операций с подходящим описанием"""
    logger.info("Запрос на поиск")
    result = []
    re_pattern = re.compile(search, re.IGNORECASE)
    for operation in data:
        if re_pattern.search(str(operation.get("Описание", ""))):
            result.append(operation)
        elif re_pattern.search(str(operation.get("Категория", ""))):
            result.append(operation)
    logger.info("Поиск успешно выполнен")
    json_data = json.dumps(result, ensure_ascii=False, indent=4)
    return json_data
