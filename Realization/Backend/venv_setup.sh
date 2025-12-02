#!/bin/bash

echo "Создаю виртуальное окружение..."
python3 -m venv venv

echo "Активирую окружение..."
source venv/bin/activate

echo "Устанавливаю зависимости..."
pip install -r requirements.txt

echo "Готово!"