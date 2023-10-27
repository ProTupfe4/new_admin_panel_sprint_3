import time
from datetime import datetime
from typing import Generator, Tuple

import backoff
from psycopg import ServerCursor
from config import APP_SETTINGS, BACKOFF_CONFIG, MOVIE_INDEX, STATE_KEY
from logger import logger
from models import Movie
from queries.filmwork import query_film
from state import State
from utils.coroutine import coroutine

from elasticsearch import helpers, Elasticsearch


@coroutine
@backoff.on_exception(**BACKOFF_CONFIG)
def fetch_changed_movies(
    cursor: ServerCursor, next_node: Generator
) -> Generator[None, str, None]:
    while last_updated := (yield):
        logger.info(
            "Querieng changed movies by several reasons greater than %s", last_updated
        )
        sql = query_film()
        cursor.execute(sql, (last_updated,))
        while result := cursor.fetchmany(size=APP_SETTINGS.batch_size):
            logger.info("Send %s records to transform step", len(result))
            next_node.send(result)


@coroutine
def transform_movies(
    next_node: Generator,
) -> Generator[None, list[dict], None]:
    while movie_dicts := (yield):
        logger.info("Transformation step begun.")
        counter = 0
        batch = []
        for movie_dict in movie_dicts:
            movie = Movie(**movie_dict).model_dump()
            movie["_id"] = movie["id"]
            batch.append(movie)
            counter += 1
        updated = movie_dicts[-1]["modified"]
        logger.info("Processed %s records", counter)
        next_node.send((batch, updated))


@coroutine
@backoff.on_exception(**BACKOFF_CONFIG)
def save_movies(
    client: Elasticsearch, state: State
) -> Generator[None, Tuple[list[dict], datetime], None]:
    while movies := (yield):
        logger.info("Loading step begun.")
        print(movies)
        t = time.perf_counter()
        lines, _ = helpers.bulk(
            client=client,
            actions=movies[0],
            index=MOVIE_INDEX,
            chunk_size=APP_SETTINGS.batch_size,
        )
        elapsed = time.perf_counter() - t
        if lines == 0:
            logger.info("Nothing to update in index %s", MOVIE_INDEX)
        else:
            logger.info(
                "%s lines was updated in %s, for index %s", lines, elapsed, MOVIE_INDEX
            )
        modified = movies[1]
        state.set_state(STATE_KEY, str(modified))
        logger.info("ES state was changed to %s date", modified)


def build_filmwork_etl(
    postgres_cursor: ServerCursor, elasticsearch_loader: Elasticsearch, state: State
):
    logger.info("==== Build film work etl pipeline started ====")
    saver_coro = save_movies(elasticsearch_loader, state)
    transformer_coro = transform_movies(next_node=saver_coro)
    fetcher_coro = fetch_changed_movies(postgres_cursor, next_node=transformer_coro)
    logger.info("==== Build film work etl pipeline completed ====")
    return fetcher_coro
