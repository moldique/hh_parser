"""
Тесты для основного модуля
"""

import pytest
from hh_parser.main import main


def test_main():
    """Тест главной функции"""
    # Пока что простой тест
    assert callable(main)

