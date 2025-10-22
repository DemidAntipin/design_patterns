from src.core.abstract_response import abstract_response
from src.core.common import common
from src.core.validator import operation_exception

# Форматирование ответа в markdown
# Первая строка ответа соответствует заголовкам - названиям полей данных в data, разделенных '|'.
# Вторая строчка ответа включает разделитель заголовка и данных.
# Третья строка содержит простые значения полей данных (int, str), разделенных '|'.
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
# Соответствует следующий markdown:
#   |unique_code|name|description|ingredients|
#   |:---|:---|:---|:---|
#   |7f4ecdab-0f01-4216-8b72-4c91d22b8918|default_recipe|step_1;ing1.unique_code|
#   ||step_2|ing2.unique_code|
#   ||step_3|ing3.unique_code|
class response_markdown(abstract_response):

    # Сформировать MARKDOWN
    def create(self, format:str, data: list):
        text = super().create(format, data)

        header = "|"

        def format_value(value):
            if hasattr(value, 'unique_code'):
               return str(value.unique_code)
            else:
                return str(value)

        # Шапка
        item = data [0]
        fields = common.get_fields( item )
        for field in fields:
            header += f"{field}|"
        header += "\n"
        text += header

        text += "|" + "|".join([":---"] * len(fields)) + "|\n"

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
                text += "|"
                for field in fields:
                    values = field_values[field]
                    if i < len(values):
                        text += f"{values[i]}|"
                    else:
                        text += "|"
                text += "\n"

        return text   