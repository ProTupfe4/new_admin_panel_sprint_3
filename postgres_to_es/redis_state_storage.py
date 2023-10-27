import json
from typing import Dict, Any

import backoff

from storage.base_state_storage import BaseStorage
from redis import Redis

from config import BACKOFF_CONFIG, STATE_ROOT


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis, name: str = STATE_ROOT):
        self.redis_adapter = redis_adapter
        self._name = name

    @backoff.on_exception(**BACKOFF_CONFIG)
    def retrieve_state(self, default_value=dict()) -> Dict[str, Any]:
        data = self.redis_adapter.get(self._name)
        if data:
            data = json.loads(data)
            return data
        return default_value

    @backoff.on_exception(**BACKOFF_CONFIG)
    def save_state(self, key: str, state: Dict[str, Any]) -> None:
        state = json.dumps(state)
        self.redis_adapter.set(self._name, state)
