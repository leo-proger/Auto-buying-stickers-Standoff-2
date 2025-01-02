import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Optional

import cv2
import mss
import numpy as np
import pyautogui
import pytesseract
import win32api
import win32con

import Config


# TODO: Сделать, чтобы координаты стикеров сами определялись в зависимости от разрешения экрана

class ImageProcessor:
    """Управляет обработкой изображения"""

    def __init__(self):
        # Можно отрегулировать числа, если случайно покупается лот
        self.gpu_canny = cv2.cuda.createCannyEdgeDetector(400, 300)
        self.gpu_borders = cv2.cuda.GpuMat()
        self.gpu_borders_gray = cv2.cuda.GpuMat()

        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH

    async def process_price(self, image: np.ndarray) -> Optional[float]:
        """Извлекает текст из изображения и преобразует в число (цену)"""
        try:
            with ThreadPoolExecutor() as executor:
                loop = asyncio.get_event_loop()
                text = await loop.run_in_executor(
                    executor,
                    lambda: pytesseract.image_to_string(image, config=Config.TESSERACT_CONFIG)
                )
            return float(text.replace(' ', ''))
        except ValueError:
            return None

    def process_edges(self, image: np.ndarray) -> np.ndarray:
        """Обрабатывает контуры изображения, используя GPU"""
        try:
            gpu_image = cv2.cuda.GpuMat()
            gpu_image.upload(image)
            gpu_image_gray = cv2.cuda.cvtColor(gpu_image, cv2.COLOR_BGRA2GRAY)
            gpu_edges = self.gpu_canny.detect(gpu_image_gray)
            return gpu_edges.download()
        finally:
            gpu_image.release()
            gpu_image_gray.release()


class MouseController:
    """Управляет всеми операциями, связанными с мышью"""

    @staticmethod
    async def buy_lot(buy_lot_y: int) -> None:
        """Покупает лот"""
        win32api.SetCursorPos((1445, buy_lot_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        win32api.SetCursorPos(Config.BUY_BUTTON_COORDINATES)
        await asyncio.sleep(0.04)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    @staticmethod
    async def periodic_double_click() -> None:
        """Периодически обновляет список лотов"""
        while True:
            await asyncio.sleep(Config.UPDATE_LOTS_BUTTON_INTERVAL)
            pyautogui.doubleClick(*Config.UPDATE_LOTS_BUTTON_COORDINATES, interval=0.1)


class ScreenCapture:
    """Управляет захватом изображения"""

    def __init__(self):
        self.sct = mss.mss()

    async def capture_screen(self, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """Захватывает часть экрана по координатам в bbox"""
        monitor = {
            "left": bbox[0],
            "top": bbox[1],
            "width": bbox[2] - bbox[0],
            "height": bbox[3] - bbox[1]
        }
        return np.array(self.sct.grab(monitor))


class StickerBot:
    """Основной класс, запускающий все процессы"""

    def __init__(self, sticker_count: Optional[int] = None, max_price: Optional[float] = None):
        self.sticker_count = sticker_count
        self.max_price = max_price

        self.stop_event = asyncio.Event()
        self.buy_lock = asyncio.Lock()

        self.image_processor = ImageProcessor()
        self.mouse_controller = MouseController()
        self.screen_capture = ScreenCapture()

    async def buy_lot(self, buy_sticker_lot_y: int) -> None:
        async with self.buy_lock:
            await self.mouse_controller.buy_lot(buy_sticker_lot_y)
            self.stop_event.set()
            print("Purchased!")

    async def check_lot_price(self, screen: np.ndarray, price_y_pos: int, buy_button_y_pos: int) -> None:
        """Проверяет цену лота и покупает, если она меньше max_price"""
        border = screen[price_y_pos:price_y_pos + 23, 0:-1]
        price_lot = await self.image_processor.process_price(border)

        if price_lot is not None and price_lot <= self.max_price:
            await self.buy_lot(buy_button_y_pos)

    async def check_lot_edges(self, screen: np.ndarray, sticker_y_pos: int, buy_button_y_pos: int) -> None:
        """Если в области screen имеется определенное количество точек, то, вероятно, это наклейка"""
        borders = screen[sticker_y_pos + 20:sticker_y_pos + 55, 0:-1]
        edges = self.image_processor.process_edges(borders)

        if np.count_nonzero(edges) > Config.BUY_STICKER_THRESHOLD:
            await self.buy_lot(buy_button_y_pos)

    async def process_stickers(self) -> None:
        """Обрабатывает стикеры"""
        bbox = Config.STICKER_BBOX[self.sticker_count]

        while not self.stop_event.is_set():
            screen = await self.screen_capture.capture_screen(bbox)
            tasks = [
                self.check_lot_edges(screen, y1, y1 + 340)
                for y1 in range(0, screen.shape[0], 78)
            ]
            await asyncio.gather(*tasks)

    async def process_prices(self) -> None:
        """Обрабатывает цены"""
        bbox_price = (1228, 351, 1274, 942)
        price_coords = [
            (0, 386), (81, 467), (162, 548), (243, 630),
            (324, 664), (405, 745), (486, 827), (567, 908)
        ]

        while not self.stop_event.is_set():
            screen = await self.screen_capture.capture_screen(bbox_price)
            tasks = [
                self.check_lot_price(screen, *coords)
                for coords in price_coords
            ]
            await asyncio.gather(*tasks)

    async def run(self) -> None:
        """Основной метод запускающий вызывающий все остальные методы в классе"""
        if self.sticker_count:
            periodic_task = asyncio.create_task(self.mouse_controller.periodic_double_click())
            await self.process_stickers()
            periodic_task.cancel()
        elif self.max_price:
            await self.process_prices()


async def main():
    mode = input("1. Купить по количеству наклеек\n2. Купить ниже определенной цены\n>>> ")

    sticker_count = None
    max_price = None

    try:
        if mode == "1":
            sticker_count_input = input("Введите количество наклеек >>> ")
            sticker_count = int(sticker_count_input)
        elif mode == "2":
            max_price_input = input("Введите цену, ниже которой надо купить лот >>> ")
            max_price = float(max_price_input)
        # TODO: Совместить 2 режима выше (покупать и с определенный количеством наклеек, и меньше какой-то цены)
    except ValueError:
        print("Введены некорректные данные. Попробуйте снова...")
        input()

    bot = StickerBot(sticker_count, max_price)
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
