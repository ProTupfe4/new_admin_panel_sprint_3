import logging

logger = logging.getLogger("etl_application")
logger.setLevel(logging.INFO)
file_hander = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s"
)

file_hander.setFormatter(formatter)
logger.addHandler(file_hander)
