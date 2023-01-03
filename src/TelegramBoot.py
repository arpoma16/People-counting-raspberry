# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import os
from dotenv import load_dotenv

load_dotenv()
# get your api_id, api_hash, token
# from telegram as described above
api_id = os.getenv( 'TELEGRAM_API_ID')
api_hash = os.getenv( 'TELEGRAM_API_HASH')
token = os.getenv( 'TELEGRAM_TOKEN')
chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))
phone = os.getenv('TELEGRAM_PHONE_NUMBER')
message = "Working.mkm.."
 
# your phone number

  
# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)
  
# connecting and building the session
client.connect()
 
# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
  
    client.send_code_request(phone)
     
    # signing in the client
    client.sign_in(phone, input('Enter the code: '))
  
  
# *** Enviar mensaje usando el ID de chat de Telegram ***
try:
    print("Creando un receptor de Telegram a partir del ID de chat de Tetlegram...")
    receptorChat = client.get_entity(chat_id)
    client.send_message(receptorChat, message)
        #Solo a modo informativo, obtenemos el nombre del Bot de Telegram al que enviamos el mensaje

 
except Exception as e:
    print("Se ha producido un error en el envío por ID de Chat: {}".format(e));
# disconnecting the telegram session
client.disconnect()

if __name__ == "__main__":
	print("ua")