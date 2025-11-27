import unittest
from src.logic.rests import rests
from src.start_service import start_service
from datetime import datetime

class test_block_date(unittest.TestCase):

    # Проверить загрузку даты блокировки из settings.json
    def test_load_block_date(self):
        # Подготовка
        service = start_service()
        service.start()

        # Действие
        block_date = service.block_date

        # Проверка
        assert block_date is not None
        assert isinstance(block_date, datetime)

    # Проверить изменение даты блокировки
    def test_change_block_date(self):
        # Подготовка
        service = start_service()
        service.start()
        rest_service = rests()
        block_date = service.block_date

        # Действие
        rest_service.update_block_date(datetime(2025, 11, 20))
        new_block_date = service.block_date

        # Проверка
        assert new_block_date is not None
        assert isinstance(new_block_date, datetime)
        assert block_date != new_block_date
        assert new_block_date == datetime(2025, 11, 20)

    # Проверить изменение остатков при изменении даты блокировки
    def test_change_block_date(self):
        # Подготовка
        service = start_service()
        service.start()
        rest_service = rests()
        date = datetime(2026, 5, 12)
        old_rests = rests().show_rests(date)

        # Действие
        rest_service.update_block_date(datetime(2025, 11, 20))
        new_rests = rests().show_rests(date)

        # Проверка
        assert isinstance(old_rests, list)
        assert isinstance(new_rests, list)
        assert len(old_rests) == len(new_rests)
        for i, rest in enumerate(old_rests):
            assert rest == new_rests[i]