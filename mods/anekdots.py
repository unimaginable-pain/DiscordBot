from ds_logger import FileLogger
import requests
from bs4 import BeautifulSoup
from discord.interactions import Interaction

anek_gen = None

class ANEKDOTY_GENERATOR:
    def __init__(self):
        self.temp_anekdoti = []
        self.anekdoti_iter = 0
        self.anekdoti_amount = 0
        self.err_code = 0
    def ANEKDOTI_NAHUY(self):
        responce = requests.get("https://www.anekdot.ru/random/anekdot/")
        if (not responce.ok):
            log.error("Не удалось загрузить анекдоты, пиздец.")
            self.err_code = responce.status_code
            return -1
        soup = BeautifulSoup(responce.text, "lxml")
        results = soup.findAll("div", class_="topicbox")
        for result in results:
            restext = result.find("div", class_="text")
            if hasattr(restext, "text"):
                self.temp_anekdoti.append(restext.text)
        self.anekdoti_amount = len(self.temp_anekdoti)
        del responce
        del soup
        log.info(f"Загружено {self.anekdoti_amount} анекдотов.")
    def ANEKDOT_NAHUY(self):
        if self.anekdoti_iter >= self.anekdoti_amount-1:
            resp = self.ANEKDOTI_NAHUY()
            if resp == -1:
                return f"Не удалось загрузить анекдоты, пиздец. ({str(self.err_code)})"
        res = self.temp_anekdoti[self.anekdoti_iter]
        self.anekdoti_iter += 1
        return res.replace("\n", " ")

async def fetch_anekdot(interaction: Interaction):
    await interaction.response.send_message(anek_gen.ANEKDOT_NAHUY())

def mod_getcommands():
    return {
        "анекдот": (fetch_anekdot, "Скинуть рофланебалу")
    }

def mod_init(logger: FileLogger):
    global log
    global anek_gen
    log = logger
    anek_gen = ANEKDOTY_GENERATOR()
    if anek_gen != None:
        log.info("Мод загружен успешно.")
