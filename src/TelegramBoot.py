# importing all required libraries
import os 
import requests

from dotenv import load_dotenv
from datetime import datetime
#from telegram import Bot

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
defauld_message = "Hello human .. 🤖 1010 1110 0110"
 
# your phone number

def Telegram_msg(msg):
    Telegram_api_sendMessage = "https://api.telegram.org/bot"+token+"/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": msg,
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None
    }
    headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json"
    }

    response = requests.post(Telegram_api_sendMessage, json=payload, headers=headers)

    print(response.text)

def telegram_DeviceOn():
    Telegram_msg("Counter ON In: 0 Out:0  Into: 0 datetime" + datetime.strftime("%Y-%m-%d, %H:%M:%S"))

def telegram_DeviceOff(input, output, into):
    Telegram_msg("Counter OFF In: "+str(input)+" Out: "+str(output)+"  Into: "+str(into)+" datetime" + datetime.strftime("%Y-%m-%d, %H:%M:%S"))

def telegram_Devicefull(count = 1):
    Telegram_msg("Room is full, people of more "+str(count))

if __name__ == "__main__":
	Telegram_msg(defauld_message)