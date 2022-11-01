import configparser
import os

main_wd = os.getcwd()

# ConfigParser с автозаполнением нужных полей, если в падлу
class AutoConfigParser:
    def __init__(self, filepath: str):
        self.fpath = filepath
        self.cfg = configparser.ConfigParser()
        if os.path.exists(filepath) and os.path.isfile(filepath):
            self.cfg.read(filepath, "utf-8")
    def get(self, section: str, field: str, fallback = "NULL"):
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        if not self.cfg[section].get(field):
            self.cfg[section][field] = fallback
            return fallback
        return self.cfg[section][field].split(" ;")[0].strip('"')
    def save(self):
        with open(self.fpath, "w", encoding="utf-8") as f:
            self.cfg.write(f)

cfg = AutoConfigParser("settings.ini")

token = cfg.get("DEFAULTS", "token")
cfg_bot_name = cfg.get("DEFAULTS", "name")
cfg_log_main = cfg.get("FILES", "main_log_file", "log.txt")
cfg_log_dir = cfg.get("FILES", "log_file_dir", "logs")
cfg_mods_dir = cfg.get("FILES", "mods_dir", "mods")
cfg_mods_log_name = cfg.get("FILES", "mods_log_name", "mod_{0}.log")
cfg_enable_message_logging = cfg.get("BOT", "enable_message_logging", "true")
cfg.save()
