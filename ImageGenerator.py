import logging
import os
import random
import uuid

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class GifInstance:
    def __init__(self, file_name):
        logger.info(f"Created gif instance by path {file_name}")
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, "rb")
        logger.info(f"file opened")
        return self.file

    def __exit__(self, exctype, excinst, exctb) -> bool:
        self.file.close()
        logger.info(f"file closed")
        os.remove(self.file_name)
        logger.info(f"file destroyed")
        return True


async def get_scramble_char():
    return chr(random.randint(33, 126))


async def get_scrambled(a: str):
    logger.info(a)
    images = [Image for i in range((len(a) + 1) * 5)]
    width = 1920 >> 2
    height = 1080 >> 2
    color_1 = 0x101010
    t_font = ImageFont.truetype('static/fonts/PTMono-Regular.ttf', 32)
    active_string = ""
    for open_chars in range(len(a) + 1):
        for iterations in range(5):
            active_string = a[:open_chars] + \
                            ''.join([await get_scramble_char() for i in range(len(a) - open_chars)])
            im = Image.new('RGB', (width, height), color_1)
            draw = ImageDraw.Draw(im)
            draw.text((width / 2, height // 2), active_string, font=t_font, anchor="mm")
            images[open_chars * 5 + iterations] = im
    images.append(images[-1])
    target_path = 'temp/gifs/' + uuid.uuid4().hex + ".gif"
    logger.debug(f"filename: {target_path}")
    durations = [80] * (len(images))
    logger.debug(target_path)
    logger.debug(os.path)
    images[0].save(
        target_path,
        format='GIF',
        disposal=2,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=durations,
        loop=1
    )
    return GifInstance(target_path)
