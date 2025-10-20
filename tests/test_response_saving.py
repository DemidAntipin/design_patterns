import pathlib
import unittest
from src.core.response_format import response_format
from src.reposity import reposity
from src.logic.factory_entities import factory_entities
from src.start_service import start_service
from src.models.settings_model import settings_model

class test_response_results_saving(unittest.TestCase):  
    # Путь до файла с тестовыми настройками
    __settings_name: str = "tests/data/settings_models.json"

    # Директория, в которую будут сохраняться файлы
    __save_directory: str = "tests/responses_results/"

    # Объект сервиса
    __start_service: start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start(self.__settings_name)

    # Автотест, создающий файлы и сохраняющий в них результаты ответов для
    # разных моделей
    def test_save_results_in_files(self):
        # Создание директории со всеми файлами
        dir_ = pathlib.Path(self.__save_directory)
        dir_.mkdir(exist_ok=True)
        settings = settings_model()
        models = reposity.keys()
        factory = factory_entities(settings)

        for format in response_format.keys():
            # Поддиректория с файлами одного формата
            subdir = dir_ / format
            subdir.mkdir(exist_ok=True)

            response = factory.create(format)()

            for model in models:
                file_path = subdir / f"{model}.{format}"
                file_path.touch(exist_ok=True)

                data = self.__start_service.data[model]
                result = response.create(format, data)
                with open(file_path, 'w', encoding="utf-8") as file:
                    file.write(result)
                    file.close()
        
  
if __name__ == '__main__':
    unittest.main() 