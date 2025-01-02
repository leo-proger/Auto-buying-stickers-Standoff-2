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


def get_mouse_clicks() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Получает координаты двух кликов мыши"""
    hwnd = find_ldplayer_window()
    if not hwnd:
        raise Exception("Окно LDPlayer не найдено!")

    window_rect = get_window_rect(hwnd)
    clicks = []

    print("1. Вам нужно кликнуть в левый верхний угол области")
    print("2. Потом в правый нижний угол области")
    print("Нажмите Esc для отмены")

    input("\nВведите что-нибудь, когда будете готовы >>> ")

    while len(clicks) < 2:
        if keyboard.is_pressed('esc'):
            print("\nОперация отменена")
            sys.exit()

        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            x, y = win32api.GetCursorPos()

            if is_point_in_window((x, y), window_rect):
                clicks.append((x, y))
                print(f"Точка {len(clicks)} зафиксирована: ({x}, {y})")

                if len(clicks) == 2:
                    break
                input("Введите что-нибудь, когда будете готовы >>> ")
            else:
                print("Клик должен быть в окне LDPlayer!")
                time.sleep(0.3)

    return clicks[0], clicks[1]


def update_config(sticker_count: int, coords: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
    """Обновляет конфигурацию в файле"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("config.json не найден. Создаём новый файл...")
        config = {}

    if 'STICKER_BBOX' not in config:
        config['STICKER_BBOX'] = {}

    # Обновляем координаты для выбранного количества наклеек
    (x1, y1), (x2, y2) = coords
    config['STICKER_BBOX'][str(sticker_count)] = [x1, y1, x2, y2]

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print(f"\nКоординаты для {sticker_count} наклеек успешно обновлены в config.json")


def main():
    print("Настройка координат области наклеек")
    try:
        while True:
            sticker_count = input("\nВведите количество наклеек (1-4) или 'q' для выхода: ")

            if sticker_count.lower() == 'q':
                break

            try:
                sticker_count = int(sticker_count)
                if not 1 <= sticker_count <= 4:
                    raise ValueError()
            except ValueError:
                print("Пожалуйста, введите число от 1 до 4")
                continue

            coords = get_mouse_clicks()
            update_config(sticker_count, coords)

            answer = input("\nХотите настроить координаты для другого количества наклеек? (y/n): ")
            if answer.lower() != 'y':
                break
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    except Exception as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()