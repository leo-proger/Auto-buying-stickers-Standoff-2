import json
from typing import Tuple, Dict


def load_config() -> dict:
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("config.json не найден")


config = load_config()

# Координаты кнопки покупки
BUY_BUTTON_COORDINATES: Tuple[int, int] = tuple(config['BUY_BUTTON_COORDINATES'])

# Порог для определения наклейки
# Если случайно покупает лоты, то повысьте значение. Если наоборот, не покупает, то уменьшите
BUY_STICKER_THRESHOLD: int = config['BUY_STICKER_THRESHOLD']

# Области для поиска наклеек
STICKER_BBOX: Dict[int, Tuple[int, int, int, int]] = {
    int(k): tuple(v) for k, v in config['STICKER_BBOX'].items()
}

# Координаты и настройки кнопки обновления лотов
UPDATE_LOTS_BUTTON_COORDINATES: Tuple[int, int] = tuple(config['UPDATE_LOTS_BUTTON_COORDINATES'])
UPDATE_LOTS_BUTTON_INTERVAL: float = config['UPDATE_LOTS_BUTTON_INTERVAL']

# Задержка обновления (выставить в соответствии с вашим интернетом. Чем он хуже, тем больше значение)
UPDATE_LOTS_BUTTON_DELAY: float = config['UPDATE_LOTS_BUTTON_DELAY']
