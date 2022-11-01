from discord.interactions import Interaction
import discord as ds
from ds_logger import FileLogger
global log
log = None

async def attachment_test(interaction, huita: ds.Attachment):
    result = f"Attachment Type: {str(huita.content_type)}"
    await interaction.response.send_message(result)

def mod_getcommands():
    return {
        "attachment_test": (attachment_test, "ебать пизда корзина")
    }

def mod_init(logger: FileLogger):
    global log
    log = logger
