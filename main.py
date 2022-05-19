from telegram.client import AuthorizationState
from telegram.client import Telegram
from fastapi import FastAPI
import getpass
import logging
import uvicorn
import time
import yaml
import os

logging.basicConfig(format='%(levelname)s - %(asctime)s:\n\t%(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)
app = FastAPI()


def instanceTelegram() -> Telegram:
    telegram: Telegram = Telegram(
        api_id=cfg["telegram"][0]["apiId"],
        api_hash=cfg["telegram"][0]["apiHash"],
        phone=cfg["telegram"][0]["phone"],
        files_directory=os.path.expanduser("~/.telegram/" + str(cfg["telegram"][0]["phone"])),
        database_encryption_key=cfg["telegram"][0]["databaseEncryptionKey"]
    )

    state = telegram.login(blocking=False)
    time.sleep(1)
    logging.debug("Comprobando el estado de retorno de la llamada de función de inicio de sesión (bloqueo = Falso)")

    if state == AuthorizationState.WAIT_CODE:
        logging.info("Se requiere PIN. En este ejemplo, el programa principal lo solicita, no el cliente de python-telegram")
        pin = input("Inserte el código PIN aquí: ")
        telegram.send_code(pin)
        state = telegram.login(blocking=False)

    if state == AuthorizationState.WAIT_PASSWORD:
        logging.info("Se requiere contraseña. En este ejemplo, el programa principal lo solicita, no el cliente de python-telegram")
        pwd = getpass.getpass('Inserte la contraseña aquí (pero asegúrese de que nadie lo esté espiando): ')
        telegram.send_password(pwd)
        state = telegram.login(blocking=False)

    logging.debug('Estado de autorización : %s', telegram.authorization_state)
    result = telegram.get_me()
    time.sleep(1)
    result.wait()
    time.sleep(1)
    return telegram


@app.get("/doCall")
def doCall(userId: int, msg: str, ):
    logging.debug("Se manda el mensaje '%s' al usuario %i", msg, userId)
    telegram: Telegram = instanceTelegram()
    time.sleep(1)
    result = telegram.call_method('createCall', {'user_id': userId, 'protocol': {'udp_p2p': True, 'udp_reflector': True, 'min_layer': 65, 'max_layer': 65}})
    time.sleep(1)
    result.wait()
    time.sleep(1)
    telegram.stop()


if __name__ == "__main__":
    with open("config.yml") as ymlFile:
        cfg = yaml.safe_load(ymlFile)
    uvicorn.run(app, host="0.0.0.0", port=30000)
