import asyncio

import cv2
import numpy as np
from PIL import ImageGrab

import Config


async def test_sticker_detection(sticker_count: int) -> None:
    while True:
        screen = np.array(await asyncio.to_thread(ImageGrab.grab, bbox=Config.STICKER_BBOX[sticker_count]))
        # screen = await asyncio.to_thread(cv2.Canny, screen, 400, 300)
        cv2.imshow('screen', screen)
        cv2.waitKey(1)


if __name__ == '__main__':
    asyncio.run(test_sticker_detection(1))
