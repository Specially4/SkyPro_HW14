import sqlite3
import json

from config import DB_PATH


def search_title(title):
    """
    title - запрос по которому выполняется поиск
    :return: - возвращает словарь содержащие данные о найденном фильме
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            sqlite_query = (f"""
                            SELECT title, country, release_year, listed_in, description, type
                            FROM netflix
                            WHERE title LIKE '%{title}%'
                            ORDER BY release_year DESC
                            LIMIT 1
            """)
            cursor.execute(sqlite_query)
            results = cursor.fetchall()
            dict_film = {}
            dict_film['title'] = results[0][0]
            dict_film['country'] = results[0][1]
            dict_film['release_year'] = results[0][2]
            dict_film['listed_in'] = results[0][3]
            dict_film['description'] = results[0][4]

    except:
        return 'Что-то пошло не так'

    else:
        return results


def search_by_years(year_1, year_2):
    """
    :param year_1: Первая граница поиска по годам
    :param year_2: Вторая граница поиска по годам
    :return: возвращает список с названием фильма и годом выпуска
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            sqlite_query = (f"""
                            SELECT title, release_year 
                            FROM netflix
                            WHERE release_year BETWEEN {year_1} AND {year_2}
                            ORDER BY release_year DESC
                            LIMIT 100
            """)
            cursor.execute(sqlite_query)
            results = cursor.fetchall()

            film_list = []
            for row in results:
                film_list.append(({'title': row[0], 'release_year': row[1]}))

    except:
        return 'Что-то пошло не так'

    else:
        return film_list


def sort_by_rating(rating):
    """
    :param rating: передаваемый рейтинг (children, family, adult)
    :return: возвращает список содержащий название, рейтинг и описание
    """
    global set_rating
    if rating in 'children':
        set_rating = ('G', '')  # Здесь добавлена пустая строка для того чтоб в условии
        # SQLite можно было искать по вхождению, далее отсеиваем дополнительным условием

    elif rating in 'family':
        set_rating = ('G', 'PG', 'PG-13')

    elif rating in 'adult':
        set_rating = ('R', 'NC-17')
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            sqlite_query = (f"""
                                SELECT title, rating, description
                                FROM netflix
                                WHERE rating IN {set_rating} 
                                AND rating != ''
                                ORDER BY rating
                            """)
            cursor.execute(sqlite_query)
            results = cursor.fetchall()

            film_list = []
            for row in results:
                film_list.append({'title': row[0], 'rating': row[1], 'description': row[2]})
    except:
        return "Что-то пошло не так"

    else:
        return film_list


def search_by_genre(genre):
    """
    :param genre: передаваемый жанр
    :return: возвращает данные в формате JSON
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            sqlite_query = (f"""
                            SELECT title, description
                            FROM netflix
                            WHERE  listed_in LIKE '%{genre}%'
                            ORDER BY release_year DESC
                            LIMIT 10
            """)
            cursor.execute(sqlite_query)
            results = cursor.fetchall()

            film = []
            for row in results:
                film.append({'title': row[0], 'description': row[1]})

    except:
        return "Что-то пошло не так"

    else:
        return json.dumps(film)


def search_cast(cast1, cast2):
    """
    :param cast1: Имя первого актера
    :param cast2: Имя второго актера
    :return: Возвращаем список актеров которые снимались с актерами переданными в функцию
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            sqlite_query = (f"""
                               SELECT "cast"
                               FROM netflix
                               WHERE "cast" LIKE '%{cast1}%' AND "cast" LIKE '%{cast2}%'
               """)
            cursor.execute(sqlite_query)
            results = cursor.fetchall()

            all_cast_list = []
            most_popular_cast = []

            """
            Далее моя голова дала сбой, и я не могу решить какой вариант решения оставить,
            мне больше нравится 1, т.к он более понятный по функционалу
            """

            for row in results:  # Данный функционал проверяет какие актеры снимались с заданными актерами более 2 раз
                all_cast_list = all_cast_list + row[0].split(', ')

            for item in all_cast_list:
                if all_cast_list.count(item) >= 2 \
                        and item not in most_popular_cast \
                        and item not in (
                cast1, cast2):  # проверяем сколько раз актеры встречаются в списке, имеются ли они
                    # в списке уже с добавленными актерами,
                    # и являются ли они актерами запроса(с последним критерием не уверен)
                    most_popular_cast.append(item)

            # for row in results:
            #     split_text = row[0].split(', ')
            # for item in split_text:
            #      if item in all_cast_list and item not in most_popular_cast:
            #          most_popular_cast.append(item)
            #
            #      if item not in all_cast_list:
            #         all_cast_list.append(item)

    except:
        return "Что-то пошло не так"

    else:
        return most_popular_cast


def list_movie(type_movie, release_year, genre):
    """
    :param type_movie: Тип картины(сериал либо фильм)
    :param release_year: Год выпуска картины
    :param genre: Жанры картины
    :return: Возвращает JSON содержащий название и описание картины
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            sqlite_query = (f"""
                            SELECT title, description
                            FROM netflix
                            WHERE type LIKE '%{type_movie}%'
                            AND release_year = '{release_year}'
                            AND listed_in LIKE '%{genre}%'
            """)

            cursor.execute(sqlite_query)
            results = cursor.fetchall()

            film_list = []
            for row in results:
                film_list.append(({'title': row[0], 'description': row[1]}))

    except:
        return "Что-то пошло не так"

    else:
        return json.dumps(film_list, indent=4)
