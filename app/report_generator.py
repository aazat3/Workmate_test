import argparse
import os
import csv
from tabulate import tabulate
from collections import defaultdict

def parse_arguments():
    """Обработка параметров скрипта."""

    parser = argparse.ArgumentParser(description="Генератор отчётов по рейтингам товаров.")
    parser.add_argument(
        "--files", nargs="+", required=True, help="Список путей к CSV-файлам с данными."
    )
    parser.add_argument(
        "--report", required=True, choices=["average-rating"], help="Тип отчёта для генерации."
    )
    return parser.parse_args()


def read_csv_files(file_paths: str) -> list[str]:
    """Читает все указанные CSV-файлы и возвращает список словарей с данными."""
    data = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            continue

        if not file_path.lower().endswith(".csv"):
            print(f"Пропущен (не CSV-файл): {file_path}")
            continue

        try:
            with open(file_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if not rows:
                    print(f"Файл пуст: {file_path}")
                else:
                    data.extend(rows)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")

    return data


def generate_average_rating_report(data: list[str]) -> None:
    """Формирует отчёт со средним рейтингом по брендам."""
    brand_ratings = defaultdict(list)

    for row in data:
        try:
            brand = row["brand"].strip()
            rating = float(row["rating"])
            brand_ratings[brand].append(rating)
        except (KeyError, ValueError):
            continue  

    report_data = []
    for brand, ratings in brand_ratings.items():
        avg_rating = sum(ratings) / len(ratings)
        report_data.append((brand, round(avg_rating, 2)))
    
    if not report_data:
        print("Файл пуст:")
    else:
        report_data.sort(key=lambda x: x[1], reverse=True)
        print(tabulate(report_data, headers=["Бренд", "Средний рейтинг"], tablefmt="github"))


def main():
    args = parse_arguments()
    data = read_csv_files(args.files)
    
    if not data:
        print("Нет данных для обработки. Проверьте файлы.")
        return
    
    if args.report == "average-rating":
        generate_average_rating_report(data)
    else:
        print("Неизвестный тип отчёта.")
        
if __name__ == "__main__":
    main()
