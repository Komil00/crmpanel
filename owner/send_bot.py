# import telebot
# token = '5437281735:AAEHwAvaEymbTUsb7GtA1DHcrBVm4mrTVWw'
# bot = telebot.TeleBot(token)
# def send(phone,code):
#     print("ishladi")
#     bot.send_message(chat_id=-1001791381186,text=f"{phone} sizning tasdiqlash kodingiz {code}")


# from eskiz_sms import EskizSMS
# from celery import shared_task


# eskiz = EskizSMS(email='komiltuev@icloud.com', password='BIxAWgiaNUTAlJFq6u6rYgm8rx12fNMt9sLm0huk',)

# @shared_task
# def send(phone, code):
#     try:
#         eskiz.send_sms(phone, code, from_whom='4546')
#         print("okay")
#         return {"status": "success"}
#     except Exception as e:
#         eskiz.send_sms(phone, code, from_whom='4546')
#         print("okay")
#         return {"status": "success"}