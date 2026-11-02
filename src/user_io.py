from abc import ABC, abstractmethod

class UserInterface(ABC):

    @abstractmethod
    def get_input(self) -> tuple[str, str, str] | None:
        """Возвращает три строки от пользователя или None (выход)."""
        ...

    @abstractmethod
    def show_result(self, triangle_type: str, vertices: list, error: str = ""):
        """Отображает результат пользователю."""
        ...
class ConsoleUserInterface(UserInterface):
    def get_input(self):
        try:
            a = input("Введите длину стороны A (или 'exit' для выхода): ").strip()
            if a.lower() in ("exit", "quit", "выход"):
                return None
            b = input("Введите длину стороны B: ").strip()
            c = input("Введите длину стороны C: ").strip()
            return a, b, c
        except Exception:
            return ("", "", "")

    def show_result(self, triangle_type: str, vertices: list, error: str = ""):
        print(triangle_type)
        print(vertices)
        if error:
            print(f"Ошибка: {error}")
        print("--------------------------------------------------------------")