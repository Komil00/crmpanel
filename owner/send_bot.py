# import telebot
# token = '5437281735:AAEHwAvaEymbTUsb7GtA1DHcrBVm4mrTVWw'
# bot = telebot.TeleBot(token)
# def send(phone,code):
#     print("ishladi")
#     bot.send_message(chat_id=-1001791381186,text=f"{phone} sizning tasdiqlash kodingiz {code}")


from eskiz_sms import EskizSMS
from django.conf import settings


eskiz = EskizSMS(
            email='komiltuev@icloud.com',
            password='BIxAWgiaNUTAlJFq6u6rYgm8rx12fNMt9sLm0huk',
        )

def send(phone, code):
    try:
        eskiz.send_sms(phone, code, from_whom='4546')
        print("okkko")
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": e}