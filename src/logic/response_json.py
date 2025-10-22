from src.core.abstract_response import abstract_response
from src.core.common import common
from src.core.validator import operation_exception
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
    def create(self, format: str, data: list):
        text = super().create(format, data)

        def format_value(value):
            if hasattr(value, 'unique_code'):
               return json.loads(self.create(format, [value]))
            elif isinstance(value, (list, tuple)):
                return [format_value(x) for x in value]
            else:
                return str(value)

        text = []
        for item in data:
            item_dict = {}
            fields = common.get_fields(item)
            for field in fields:
                value = getattr(item, field)
                item_dict[field] = format_value(value)
            text.append(json.dumps(item_dict, ensure_ascii=False))
        
        if len(text)>1:
            return "["+','.join(text)+"]"
        else:
            return text[0]