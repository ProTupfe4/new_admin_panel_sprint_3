import time
from contextlib import closing
from datetime import datetime

import backoff
import psycopg
from elasticsearch import Elasticsearch
from psycopg import ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from redis import Redis

from config import (
    BACKOFF_CONFIG,
    POSTGRES_DSN,
    ELASTIC_DSN,
    REDIS_DSN,
    STATE_KEY,
    STATE_ROOT,
    APP_SETTINGS,
)
from logger import logger
from filmwork_pipeline import build_filmwork_etl
from state import State
from redis_state_storage import RedisStorage


@backoff.on_exception(**BACKOFF_CONFIG)
def main() -> None:
    postgres_dsn = make_conninfo(**POSTGRES_DSN.model_dump())
    elastic_dsn = f"http://{ELASTIC_DSN.host}:{ELASTIC_DSN.port}"
    redis_client = Redis(**REDIS_DSN.model_dump())
    state = State(RedisStorage(redis_client, STATE_ROOT))
    with closing(
        psycopg.connect(postgres_dsn, row_factory=dict_row)
    ) as conn, ServerCursor(conn, "fetcher") as cursor, closing(
        Elasticsearch([elastic_dsn])
    ) as elastic_client:
        coro = build_filmwork_etl(
            postgres_cursor=cursor, elasticsearch_loader=elastic_client, state=state
        )
        while True:
            last_update = state.get_state(STATE_KEY)
            logger.info(
                "==== STARTING ETL PROCESS FOR UPDATES.... Last Update was %s",
                last_update,
            )
            if last_update is None:
                last_update = datetime.min

            coro.send(str(last_update))
            time.sleep(APP_SETTINGS.scan_frequency)


if __name__ == "__main__":
    main()
