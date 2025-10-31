from src.core.abstract_response import abstract_response
from src.core.common import common
from src.core.validator import operation_exception
from src.logic.factory_converters import factory_converters
from src.core.response_format import response_format
import json

# Форматирование ответа в json
# 
# Например рецепту
#   class recipe():
#       unique_code = "7f4ecdab-0f01-4216-8b72-4c91d22b8918"
#       name = "default_recipe"
#       description = ["step_1","step_2","step_3"]
#       ingredients = [ing1, ing2, ing3]
#   } 
#
# Соответствует следующий json:
#   {
#      unique_code: "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#      name: "default_recipe",
#      description: [
#                       "step_1",
#                       "step_2",
#                       "step_3"
#                   ],
#      ingredients: [
#                       {
#                           unique_code: ing1.unique_code,
#                           name: ing1.name,
#                           nomenclature: ing1.nomenclature,
#                           value: ing1.value
#                       },
#                       {
#                           unique_code: ing2.unique_code,
#                           name: ing2.name,
#                           nomenclature: ing2.nomenclature,
#                           value: ing2.value
#                       },
#                       {
#                           unique_code: ing3.unique_code,
#                           name: ing3.name,
#                           nomenclature: ing3.nomenclature,
#                           value: ing3.value
#                       }
#                   ]
#   }
class response_json(abstract_response):
    
    # Сформировать JSON
    def create(self, data: list):
        text = super().create(response_format.json_format(), data)

        factory = factory_converters()

        return json.dumps(factory.convert(data), ensure_ascii=False)