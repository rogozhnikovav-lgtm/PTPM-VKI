import logging
import sys
import os

from TriangleValid import TriangleCalculator
from Database import TriangleDatabase
from user_io import ConsoleUserInterface
from notifier import MockEmailNotifier
from controller import Controller


LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "triangle_log.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)


def main():
    controller = Controller(
        calculator=TriangleCalculator(),
        db=TriangleDatabase(),
        ui=ConsoleUserInterface(),
        notifier=MockEmailNotifier(),
    )
    logging.info("Приложение запущено")

    while True:
        result = controller.run_once()
        if result == "exit":
            print("Программа завершена.")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.critical("Критическая ошибка в работе программы")
        logging.exception("Трассировка стека:")
        sys.exit(1)