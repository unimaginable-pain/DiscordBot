#!/usr/bin/python3
#работает и отдельно бтв
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import os
import enum
from io import BytesIO
import sys
import discord as ds
from discord.interactions import Interaction
from pygifsicle import gifsicle
from tempfile import _get_candidate_names
import asyncio
from discord.errors import HTTPException

global log
log = None

class TextPosition(enum.Enum):
    TOP = 1
    BOTTOM = 2

def _add_text_to_gif(gif: ImageSequence.Iterator, text: str, font, textpos: TextPosition = TextPosition.BOTTOM) -> BytesIO:
    if not text or not text.strip():

        return "Поле текста не может быть пустым"
    if gif == None:
        return "debug error: поле gif = None"
    if font == None:
        return "debug error: поле font = None"
    width = font.getlength(text)
    height = font.size
    x = (gif[0].width - width) / 2
    y = 0
    if textpos == TextPosition.BOTTOM:
        y = gif[0].height - height - 10
    elif textpos == TextPosition.TOP:
        y = 0
    frames = []
    for frame in gif:
        frame = frame.convert("RGB")
        dr = ImageDraw.Draw(frame)
        dr.text((x, y), text, fill=(255, 255, 255), font=font)
        del dr
        frames.append(frame)
    res = BytesIO()
    frames[0].save(res, format="GIF", save_all=True, append_images=frames[1:])
    return res

def add_text_to_gif(gif: ImageSequence.Iterator | os.PathLike, text: str, font: str | ImageFont.FreeTypeFont, size: int = 25, pos: TextPosition = TextPosition.BOTTOM):
    if isinstance(gif, str):
        _iter = ImageSequence.Iterator(Image.open(gif))
    else:
        _iter = gif
    if isinstance(font, str):
        _font = ImageFont.truetype(f"/usr/share/fonts/TTF/{font}.ttf", size)
    else:
        _font = font
    if isinstance(pos, str):
        if (pos == "сверху"):
            _pos = TextPosition.TOP
        else:
            _pos = TextPosition.BOTTOM
    else:
        _pos = pos
    return _add_text_to_gif(_iter, text, _font, _pos)

async def add_text_to_gif_discord(interaction: Interaction, гифка: ds.Attachment, текст: str, шрифт: str, размер: int = 50, положение: str = "снизу"):
    await interaction.response.send_message("В процессе")
    pos = положение.lower()
    if "gif" not in гифка.content_type:
        await interaction.edit_original_response(content="Гифку скинь, кому сказано.")
        return "Гифку скинь, кому сказано."
    f_name = f"cache/{next(_get_candidate_names())}.gif"
    f_name_out = f"cache/{next(_get_candidate_names())}.gif"
    f = open(f_name, 'wb')
    f.write(await гифка.read())
    f.close()
    result = add_text_to_gif(ImageSequence.Iterator(Image.open(f_name)), текст, шрифт, размер, pos)
    result.seek(0)
    f = open(f_name, 'wb')
    f.write(result.read())
    f.close()
    gifsicle(
        sources=f_name,
        destination=f_name_out,
        optimize=True,
        options=["--lossy"]
    )
    res_f = open(f_name_out, 'rb')
    asyncio.run(interaction.edit_original_response(content="Готово", attachments=[ds.File(fp=res_f, filename="result.gif")]))
    print("deleting...")
    res_f.close()
    os.remove(f_name)
    os.remove(f_name_out)

def mod_getcommands():
    return {
        "тексткгифке": (add_text_to_gif_discord, "Добавить текст к гифке")
    }

def mod_init(logger):
    global log
    log = logger
    if not os.path.exists("cache") or not os.path.isdir("cache"):
        os.mkdir("cache")
    log.info("Мод загружен успешно")

#если запускать этот скрипт отдельно
if __name__ == "__main__":
    gif = sys.argv[1]
    text = sys.argv[2]
    font = sys.argv[3]
    size = int(sys.argv[4])
    result = add_text_to_gif(gif, text, font, size)
    f = open(f"{gif}1.gif", 'wb')
    f.write(result.getvalue())
    f.close()
