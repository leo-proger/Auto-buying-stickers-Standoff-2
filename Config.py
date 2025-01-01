from typing import Tuple

TESSERACT_PATH: str = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSERACT_CONFIG: str = r'--oem 3 --psm 6'

BUY_BUTTON_COORDINATES: Tuple[int, int] = (1073, 666)
BUY_STICKER_THRESHOLD: int = 72  # Если случайно покупает лоты, то повысьте значение. Если наоборот, не покупает, то уменьшите
STICKER_BBOX = {
    1: (1169, 335, 1206, 930),
    2: (1134, 335, 1171, 930),
    3: (1100, 335, 1137, 930),
    4: (1065, 335, 1102, 930),
}

UPDATE_LOTS_BUTTON_COORDINATES: Tuple[int, int] = (780, 290)
UPDATE_LOTS_BUTTON_INTERVAL: float = 5.0
UPDATE_LOTS_BUTTON_DELAY: float = 0.001  # Выставить в соответствии с вашим интернетом. Чем он хуже, тем больше значение
