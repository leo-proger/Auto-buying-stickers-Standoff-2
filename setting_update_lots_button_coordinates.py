import json
import sys
from typing import Optional, Tuple
import win32gui
import win32api
import win32con
import keyboard
import time


def find_ldplayer_window() -> Optional[int]:
    """Находит окно LDPlayer"""
    return win32gui.FindWindow(None, "LDPlayer")


def get_window_rect(hwnd: int) -> Tuple[int, int, int, int]:
    """Получает координаты окна"""
    return win32gui.GetWindowRect(hwnd)


def is_point_in_window(point: Tuple[int, int], window_rect: Tuple[int, int, int, int]) -> bool:
    """Проверяет, находится ли точка в пределах окна"""
    x, y = point
    left, top, right, bottom = window_rect
    return left <= x <= right and top <= y <= bottom


def get_button_click() -> Tuple[int, int]:
    """Получает координаты клика мыши для кнопки обновления"""
    hwnd = find_ldplayer_window()
    if not hwnd:
        raise Exception("Окно LDPlayer не найдено!")

    window_rect = get_window_rect(hwnd)

    print("\nВам нужно кликнуть на кнопку обновления лотов")
    input("\nВведите что-нибудь, когда будете готовы >>> ")

    while True:
        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            x, y = win32api.GetCursorPos()

            if is_point_in_window((x, y), window_rect):
                return x, y
            else:
                print("Клик должен быть в окне LDPlayer!")
                time.sleep(0.3)
        time.sleep(0.1)


def update_config(coords: Tuple[int, int]) -> None:
    """Обновляет конфигурацию в файле"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("config.json не найден. Создаём новый файл...")
        config = {}

    # Обновляем координаты кнопки обновления
    config['UPDATE_LOTS_BUTTON_COORDINATES'] = list(coords)

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print(f"\nКоординаты {coords} кнопки обновления успешно обновлены в config.json")


def main():
    try:
        print("Настройка координат кнопки обновления лотов")
        coords = get_button_click()
        update_config(coords)

    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    except Exception as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()