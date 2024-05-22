import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(group_name: str, log_level: str):
    """
    Настроить логгер для определенной группы и уровня логирования.

    :param group_name: Имя группы (например, 'bot' или 'phone').
    :param log_level: Уровень логирования ('INFO', 'WARNING', 'ERROR').
    """

    # Создать папку для группы, если ее нет
    if not os.path.exists(f'logs/{group_name}'):
        os.makedirs(f'logs/{group_name}')

    # Создать и настроить логгер
    logger_name = f"{group_name}_{log_level.lower()}"
    logger = logging.getLogger(logger_name)

    # Настроить форматтер
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Если уровень логирования INFO, сохраняем в отдельный файл
    if log_level == 'INFO':
        file_name = f'logs/{group_name}/info.log'
    else:
        file_name = f'logs/{group_name}/other.log'

    # Настроить обработчик для файла
    file_handler = RotatingFileHandler(file_name, maxBytes=int(3e7), backupCount=15)
    file_handler.setFormatter(formatter)

    if log_level == 'INFO':
        file_handler.setLevel(logging.INFO)
    else:
        file_handler.setLevel(logging.WARNING)

    # Удаляем старые обработчики, если они есть, чтобы избежать дублирования логов
    logger.handlers = []

    # Добавить обработчики
    logger.addHandler(file_handler)

    logger.setLevel(log_level)

    return logger