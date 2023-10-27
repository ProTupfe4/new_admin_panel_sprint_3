from typing import Optional


def query_film():
    return f"""
    SELECT film.id, film.rating AS imdb_rating, film.title, film.description,
    ARRAY_AGG(DISTINCT genre.name) as genre,
    ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'director') AS director,
    ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'actor') AS actors_names,
    ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'screenwriter' ) AS writers_names,
    ARRAY_AGG(
        DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name))
     FILTER (WHERE person_film.role = 'actor') AS actors,
    ARRAY_AGG(
        DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name))
     FILTER (WHERE person_film.role = 'screenwriter') AS writers,
     GREATEST(film.modified, MAX(genre.modified), MAX(person.modified)) as modified
    FROM content.film_work film 
    LEFT JOIN content.genre_film_work AS genre_film ON film.id = genre_film.film_work_id
    LEFT JOIN content.genre AS genre ON genre_film.genre_id = genre.id
    LEFT JOIN content.person_film_work AS person_film ON person_film.film_work_id = film.id
    LEFT JOIN content.person AS person ON person_film.person_id = person.id
    WHERE GREATEST(film.modified, genre.modified, person.modified) > %s
    GROUP BY film.id
    ORDER BY modified ASC
    """
