import json
from json import JSONDecodeError
from logging import Logger

from .base_state_storage import BaseStorage


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, испольующего локальный файл

    Формат хранения: JSON
    """

    def __init__(self, logger: Logger, file_path: str):
        self.file_path = file_path
        self._logger = logger

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище"""
        with open(self.file_path, 'w') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, 'w') as json_file:
                return json.load(json_file)
        except (FileNotFoundError, JSONDecodeError):
            self._logger.warning(
                'No correct state file provided. Continue with default'
            )
            return dict()
