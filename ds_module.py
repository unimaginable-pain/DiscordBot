import asyncio
from typing import Callable, Dict, Tuple
from ds_logger import FileLogger
from ds_constants import cfg_mods_log_name, cfg_mods_dir
import os
import discord as ds

class ModuleWrapper:
    def __init__(self):
        self.command_table: dict[str, Tuple[Callable, str]] = {}
    def add_module(self, name):
        mod = Module(name)
        cmds = mod.get_commands()
        self.appcommandtable = []
        for cmdname, cmd in cmds.items():
            appcommand = ds.app_commands.Command(name=cmdname, description=cmd[1], callback=cmd[0])
            self.appcommandtable.append(appcommand)
        self.command_table.update(cmds)
        return self.appcommandtable

class Module:
    def __enter__(self):
        return self
    def __exit__(self):
        if self.file != None:
            self.file.close()
            del self.file
    def __init__(self, filename: str):
        self.filename = filename
        if not os.path.exists(os.path.join(cfg_mods_dir, self.filename)
            or not os.path.isfile(os.path.join(cfg_mods_dir, self.filename))):
            raise FileNotFoundError("Файл не существует. Как эта ошибка произошла?") # эта ошибка не может произойти без ручного вмешательства
        strippedname = filename[:filename.find('.')]
        self.mod = __import__(strippedname) # обычный import здесь не сработает, т. к. нужен именно объект модуля
        if hasattr(self.mod, "MOD_NAME"):
            self.name = self.mod.MOD_NAME
        else:
            self.name = strippedname
        if not hasattr(self.mod, "mod_init"):
            raise Exception("Инициализирующая функция модуля не найдена")
        self.logger = FileLogger(cfg_mods_log_name.format(self.name))
        self.mod.mod_init(self.logger)
    def get_commands(self) -> Dict[str, Tuple[Callable, str]]:
        if hasattr(self.mod, "mod_getcommands"):
            return self.mod.mod_getcommands()
