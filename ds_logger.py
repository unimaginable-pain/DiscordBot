from typing import IO
from ds_constants import main_wd, cfg_log_dir
import datetime
import os
import io
import sys

toConsole = False
if "--console" in sys.argv:
    toConsole = True

class FileLogger:
    def __init__(self, logfile: str):
        if logfile == "" or logfile == None:
            self.handle = None
            return
        fullpath = os.path.join(main_wd, cfg_log_dir, logfile)
        if not toConsole:
            self.handle = open(fullpath, "a", encoding="utf-8")
        else:
            self.handle = sys.stdout
    def log(self, status: str, msg: str):
        res = self.handle.write(
            f"{datetime.datetime.now().strftime('[%d %b %Y, %H:%M:%S')} {status}] {msg}\n")
        self.handle.flush()
        return res
    def info(self, msg: str):
        return self.log("INFO", msg)
    def warn(self, msg: str):
        return self.log("WARN", msg)
    def error(self, msg: str):
        return self.log("ERROR", msg)
    def __del__(self):
        self.handle.close()
    def redirect(self, io_obj: IO):
        if not isinstance(io_obj, io.IOBase):
            raise IOError("redirected to not writable")
