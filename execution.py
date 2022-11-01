from typing import List
import nest_asyncio
nest_asyncio.apply()
import sys
import discord as ds
from ds_constants import *
import os
import asyncio
from ds_module import ModuleWrapper
from ds_logger import FileLogger
main_logger = FileLogger(cfg_log_main)

globalLock = True
finallyEnd = False

class DiscordBot:
    def __init__(self, token, apps: List[ds.app_commands.Command]):
        intents = ds.Intents.all()
        intents.messages = True
        self.cl = ds.Client(intents = intents)
        if not token or token == "NULL":
            main_logger.error("Необходимо указать токен в файле настроек.")
            exit(1)
        self.tk = token
        self.command_tree = ds.app_commands.CommandTree(self.cl)
        for x in apps: # загрузка всех слеш-команд в CommandTree
            main_logger.info(f"Загружена команда {x.name}.")
            self.command_tree.add_command(x)
        @self.cl.event
        async def on_message(message: ds.Message):
            # если сообщение не от бота, то записать в логи
            if not cfg_enable_message_logging:
                return
            if message.author.id != self.cl.user.id and len(message.content) > 0:
                main_logger.info(f"Сообщение ({message.author.name}): {message.content}")
            # сообщения с префиксом удалены в связи с переходом на слеш-команды
        @self.cl.event
        async def on_ready():
            await self.command_tree.sync()
            main_logger.info("Инициализированно дерево комманд.")
            print(f"\n{cfg_bot_name} начал работу.")
            global globalLock
            globalLock = False
            pass
    def run(self):
        self.cl.run(self.tk)

async def main():
    # Чекаем все пайтон файлы в директории mods
    main_logger.info(f"{cfg_bot_name} подгружает моды...")
    sys.path.append(cfg_mods_dir) # добавить папку, из которой можно подгружать моды
    try:
        # перебор всех файлов .py в папке модов
        modules = [x for x in os.listdir(cfg_mods_dir) if os.path.isfile(os.path.join(cfg_mods_dir, x)) and x.endswith(".py")]
    except FileNotFoundError:
        modules = []
        main_logger.warn(f"Не найдена папка модов \"{cfg_mods_dir}\".")
        os.makedirs(cfg_mods_dir, 0o777, True)
    wrapper = ModuleWrapper()
    loadedapps = [] # Apps здесь Application Commands (слеш команды)
    for module in modules:
        apps = None # команды в моде
        try:
            apps = wrapper.add_module(module)
            main_logger.info(f"Загружен мод {module}.")
        except Exception as e:
            main_logger.error(f"Не удалось загрузить \"{module}\" ({str(e).capitalize()}).")
            continue
        if apps != None:
            for app in apps:
                loadedapps.append(app)
    main_logger.info(f"Загружено {str(len(modules))} модов.")
    bot = DiscordBot(token, loadedapps)
    bot.run()
    # не ебу че это, боюсь убирать
    while not finallyEnd:
        await asyncio.sleep(1)
    return 0

res = asyncio.run(main())
exit(1)
