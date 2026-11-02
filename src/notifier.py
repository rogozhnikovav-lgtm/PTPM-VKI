from abc import ABC, abstractmethod
import logging


class ExternalNotifier(ABC):
    """Абстрактный интерфейс сторонней зависимости (email-сервер и т.п.)."""

    @abstractmethod
    def send(self, message: str) -> bool:
        """Имитация отправки данных стороннему процессу."""
        ...


class MockEmailNotifier(ExternalNotifier):
    """Имитация отправки на email-сервер."""

    def send(self, message: str) -> bool:
        logging.info(f"[MOCK EMAIL] Отправка сообщения: {message}")
        print(f"[Имитация отправки на email]: {message}")
        return True