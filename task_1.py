import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()


def test_add_new_book_with_valid_name(collector):
    collector.add_new_book("Маленький принц")
    assert "Маленький принц" in collector.books_genre
    assert collector.books_genre["Маленький принц"] == ""


@pytest.mark.parametrize("invalid_name", ["", "А" * 41])
def test_add_new_book_rejects_invalid_name(collector, invalid_name):
    collector.add_new_book(invalid_name)
    assert invalid_name not in collector.books_genre


def test_add_new_book_does_not_overwrite_existing(collector):
    collector.add_new_book("1984")
    collector.set_book_genre("1984", "Фантастика")
    collector.add_new_book("1984")
    assert collector.books_genre["1984"] == "Фантастика"


def test_set_book_genre_only_for_exsiting_books_and_valid_genres(collector):
    collector.add_new_book("Сияние")
    collector.set_book_genre("Сияние", "Ужасы")
    assert collector.books_genre["Сияние"] == "Ужасы"

    collector.set_book_genre("Неизвестная книга", "Фантастика")
    assert "Неизвестная книга" not in collector.books_genre


def test_get_book_genre_returns_correct_genre(collector):
    collector.add_new_book("Шерлок Холмс")
    collector.set_book_genre("Шерлок Холмс", "Детективы")
    assert collector.get_book_genre("Шерлок Холмс") == "Детективы"


def test_get_books_with_specific_genre_filters_correctly(collector):
    collector.add_new_book("Интерстеллар")
    collector.set_book_genre("Интерстеллар", "Фантастика")
    collector.add_new_book("Монстр")
    collector.set_book_genre("Монстр", "Ужасы")
    assert collector.get_books_with_specific_genre("Фантастика") == ["Интерстеллар", "Монстр"]


def test_get_books_for_children_excludes_age_restricted(collector):
    collector.add_new_book("Коралина")
    collector.set_book_genre("Коралина", "Ужасы")
    collector.add_new_book("Король Лев")
    collector.set_book_genre("Король Лев", "Мультфильмы")
    assert collector.get_books_for_children() == ["Король Лев"]


def test_add_book_in_favorites_only_once(collector):
    collector.add_new_book("Малыш и Карлсон")
    collector.add_book_in_favorites("Малыш и Карлсон")
    collector.add_book_in_favorites("Малыш и Карлсон")
    assert collector.get_list_of_favorites_books() == ["Малыш и Карлсон"]


def test_delete_book_from_favorites_removes_correctly(collector):
    collector.add_new_book("Приключения Тома Сойера")
    collector.add_book_in_favorites("Приключения Тома Сойера")
    collector.delete_book_from_favorites("Приключения Тома Сойера")
    assert collector.get_list_of_favorites_books() == []


def test_get_books_genre_returns_full_mapping(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    result = collector.get_books_genre()
    assert result == {"Гарри Поттер": "Фантастика"}