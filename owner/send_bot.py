import telebot
token = '5437281735:AAEHwAvaEymbTUsb7GtA1DHcrBVm4mrTVWw'
bot = telebot.TeleBot(token)
def send(phone,code):
    print("ishladi")
    bot.send_message(chat_id=-1001791381186,text=f"{phone} sizning tasdiqlash kodingiz {code}")
