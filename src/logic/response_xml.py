import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.core.abstract_response import abstract_response
from src.core.common import common
import html


# Форматирование ответа в xml
# 
# Исходным тегом является <object>
# Названия других тегов соответствуют названиям полей объекта
# Каждый элемент массива заключается в тег <item></item>
# К вложенным объектам рекурсивно применяется формирование xml ответа.
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
# <root>
#   <object>
#      <unique_code>7f4ecdab-0f01-4216-8b72-4c91d22b8918</unique_code>
#      <name>default_recipe</name>
#      <description>
#          <item>step_1</item>
#          <item>step_2</item>
#          <item>step_3</item>
#      </description>
#      <ingredients>
#           <item>
#                 <object>
#                     <unique_code>ing1.unique_code</unique_code>
#                     <name>ing1.name</name>
#                     <nomenclature>ing1.nomenclature</nomenclature>
#                     <value>ing1.value</value>
#                 </object>
#           </item>
#           <item>
#                 <object>
#                     <unique_code>ing2.unique_code</unique_code>
#                     <name>ing2.name</name>
#                     <nomenclature>ing2.nomenclature</nomenclature>
#                     <value>ing2.value</value>
#                 </object>
#           </item>
#           <item>
#                 <object>
#                     <unique_code>ing2.unique_code</unique_code>
#                     <name>ing2.name</name>
#                     <nomenclature>ing2.nomenclature</nomenclature>
#                     <value>ing2.value</value>
#                 </object>
#           </item>
#      </ingredients>
#   </object>
# </root>
class response_xml(abstract_response):
    
    # Сформировать XML
    def create(self, format: str, data: list, __is_root=True):
        text = super().create(format, data)
        
        def format_value(value):
            if hasattr(value, 'unique_code'):
               return html.unescape(self.create(format, [value], False))
            else:
                return str(value)

        for item in data:
            object = ET.Element('object')
            fields = common.get_fields(item)
            for field in fields:
                field_element = ET.SubElement(object, field)
                value = getattr(item, field)
                if isinstance(value, list):
                    for v in value:
                        list_item_element = ET.SubElement(field_element, 'item')
                        try:
                            list_item_element.append(ET.fromstring(format_value(v)))
                        except:
                            list_item_element.text = format_value(v)
                else:
                    field_element.text = format_value(value)
            text += html.unescape(ET.tostring(object, encoding="unicode"))
        if __is_root:
            text = f'<?xml version="1.0" encoding="unicode"?><root>{text}</root>'
        return text