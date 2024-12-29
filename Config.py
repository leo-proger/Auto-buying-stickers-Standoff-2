from typing import Tuple

TESSERACT_PATH: str = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSERACT_CONFIG: str = r'--oem 3 --psm 6'

BUY_BUTTON_COORDINATES: Tuple[int, int] = (1073, 666)
STICKER_BBOX = {
    1: (1188, 335, 1225, 930),
    2: (1151, 335, 1188, 930),
    3: (1119, 335, 1156, 930),
    4: (1084, 335, 1121, 930),
}

UPDATE_LOTS_BUTTON_COORDINATES: Tuple[int, int] = (761, 306)
UPDATE_LOTS_BUTTON_INTERVAL: float = 15.0
