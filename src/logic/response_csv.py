from src.core.abstract_response import abstract_response
from src.core.common import common
from src.core.validator import operation_exception
from src.core.response_format import response_format

# Форматирование ответа в csv
# Первая строка ответа соответствует названиям полей данных в data, разделенных ';'.
# Вторая строка содержит простые значения полей данных (int, str), разделенных ';'.
# Значения типа list записаются в несколько строчек, где каждая строчка соответствует значению 1 элемента list.
# Вместо значений классов записывается unique_code класса.
# 
# Например рецепту
#   class recipe():
#       unique_code = "7f4ecdab-0f01-4216-8b72-4c91d22b8918"
#       name = "default_recipe"
#       description = ["step_1","step_2","step_3"]
#       ingredients = [ing1, ing2, ing3]
#   } 
#
# Соответствует следующий csv:
#   unique_code;name;description;ingredients;
#   7f4ecdab-0f01-4216-8b72-4c91d22b8918;default_recipe;step_1;ing1.unique_code;
#   ;;step_2;ing2.unique_code;
#   ;;step_3;ing3.unique_code;
class response_csv(abstract_response):

    # Сформировать CSV
    def create(self, data: list):
        text = super().create(response_format.csv_format(), data)

        # Шапка
        item = data[0]
        fields = common.get_fields(item)
        for field in fields:
            text += f"{field};"
        text += "\n"

        # Форматирование значения
        def format_value(value):
            if hasattr(value, 'unique_code'):
               return str(value.unique_code)
            else:
                return str(value)

        # Данные
        for item in data:
            field_values = {}
            max_list_length = 1
            item_fields = common.get_fields(item)
            if fields != item_fields:
                raise operation_exception("Количество и/или названия полей объектов не совпадают.")
            for field in fields:
                value = getattr(item, field)
                if isinstance(value, list):
                    field_values[field] = [format_value(v) for v in value]
                    max_list_length = max(max_list_length, len(value))
                else:
                    field_values[field] = [format_value(value)]
            for i in range(max_list_length):
                for field in fields:
                    values = field_values[field]
                    if i < len(values):
                        text += f"{values[i]};"
                    else:
                        text += ";"
                text += "\n"

        return text