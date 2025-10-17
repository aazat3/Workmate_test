1) Активация виртуального окружения 
.venv/Scripts/Activate.ps1

2) Установка пакетов
pip install -r requirements.txt

3) Запуск скрипта
python app/report_generator.py --files files//products1.csv files//products2.csv --report average-rating

4) Тестирование
pytest -v