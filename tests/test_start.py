import unittest
from src.start_service import start_service
from src.reposity import reposity
from src.models.measure_model import measure_model
import os
import json
import tempfile


# Набор тестов для проверки работы статового сервиса
class test_start(unittest.TestCase):

    # Проверить создание start_service и заполнение данными
    def test_notThow_start_service_load(self):
        # Подготовка
        start = start_service()

        # Действие
        start.start()

        # Проверка
        assert len(start.data[ reposity.measure_key()]) > 0

    # Проверить уникальность элементов
    def test_checkUnique_start_service_load(self):
        # Подготовка
        start = start_service()

        # Действие
        start.start()

        # Проверка
        gramm =  list(filter(lambda x: x.name == "Грамм", start.data[ reposity.measure_key()])) 
        kg =  list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.measure_key()])) 
        assert gramm[0].unique_code == kg[0].base_unit.unique_code


    # Проверить метод keys класса reposity
    def test_any_reposity_keys(self):
        # Подготовка

        # Действие
        result = reposity.keys()
        
        # Проверка
        assert len(result) > 0

    # Проверить метод initalize класса reposity 
    def test_notThrow_reposity_initialize(self):   
        # Подготовка
        repo = reposity()

        # Действие
        repo.initalize() 

    # Проверить First_start
    def test_first_start_start_service(self):
        # Подготовка
        service = start_service()
        service.repo = reposity()
        service.first_start = True
        service.repo.initalize()

        # Действие

        # Проверки
        assert service.first_start == True
        service.start()
        assert service.first_start == False

    # Проверить пропуск загрузки данных, если запуск не первый
    def test_skip_data_load_start_service(self):
        # Подготовка
        service = start_service()
        service.repo = reposity()
        service.repo.initalize()

        # Действие
        service.start(file="tests/data/not_first_start.json")

        # Проверки
        for key in service.data.keys():
            assert len(service.data[key]) == 0

    # Проверить сохранение данных репозитория
    # Файл создается и json с ключами, соответствующими reposity.keys()
    def test_create_file_saving_reposity_start_service(self):
        # Подготовка
        service = start_service()
        service.start()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            file_path = tmp_file.name

        # Действие
        service.save_reposity(file_path)

        # Проверки
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for key in service.data.keys():
            assert key in data
        
        os.remove(file_path)
        