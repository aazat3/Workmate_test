import pytest
import csv
from app.report_generator import read_csv_files, generate_average_rating_report, parse_arguments


# --- Вспомогательные функции ---
@pytest.fixture
def sample_csv(tmp_path):
    """Создаёт временный CSV-файл с тестовыми данными."""
    data = [
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", "999", "4.9"],
        ["galaxy s23 ultra", "samsung", "1199", "4.8"],
        ["redmi note 12", "xiaomi", "199", "4.6"],
    ]
    file_path = tmp_path / "sample.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return file_path


# --- Тесты чтения CSV ---
def test_read_csv_files_success(sample_csv):
    data = read_csv_files([str(sample_csv)])
    assert len(data) == 3
    assert data[0]["name"] == "iphone 15 pro"
    assert data[0]["brand"] == "apple"
    assert data[0]["price"] == "999"
    assert data[0]["rating"] == "4.9"


def test_read_csv_file_not_found(tmp_path):
    fake_file = tmp_path / "missing.csv"
    data = read_csv_files([str(fake_file)])
    assert data == []


def test_read_csv_not_csv_extension(tmp_path):
    fake_file = tmp_path / "wrong.txt"
    fake_file.write_text("some text")
    data = read_csv_files([str(fake_file)])
    assert data == []


# --- Тест формирования отчёта ---
def test_generate_average_rating_report_output(capsys, sample_csv):
    data = read_csv_files([str(sample_csv)])
    generate_average_rating_report(data)
    output = capsys.readouterr().out
    assert "apple" in output
    assert "Средний рейтинг" in output
    assert "| apple" in output  


def test_generate_average_rating_report_empty(capsys):
    generate_average_rating_report([])
    output = capsys.readouterr().out
    assert "Файл пуст:" in output


# --- Тест аргументов ---
def test_parse_arguments_valid(monkeypatch):
    test_args = ["prog", "--files", "a.csv", "--report", "average-rating"]
    monkeypatch.setattr("sys.argv", test_args)
    args = parse_arguments()
    assert args.report == "average-rating"
    assert "a.csv" in args.files


def test_parse_arguments_invalid_report(monkeypatch):
    test_args = ["prog", "--files", "a.csv", "--report", "wrong-report"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        parse_arguments()
