from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from pyrogram import Client, filters

bot = 'my_bot'  # tg bot username
# bot = f't.me/{user}'
app = Client(bot)

USERS = {
    4643643346: {
        'phone': '+999999999',
        'fio': 'John Doe'
    }
}

STEPS = {
    4643643346: ''
}

APPEALS = {
    4643643346: {
        'reason': '',
        'video': '',
    }
}

BUTTONS = {
    'send_number': "Send my phone number",
    'check_result': "check my result data"
}

TEXTS = {
    'welcome': "Hi send me your phone number",
    'wanna': "wanna check your data?",
    'fio': "Please write your fullname",
    'reason': "write the reason for your displeasure",
    'video': "send your video message",
    'thanks': "Thank you for your reason!",
    'wrong_video': "something go wrong pls retry your video"
}


@app.on_message(filters.command('start'))
def welcome_user(client, message):
    message.reply_text(TEXTS['welcome'], reply_markup=ReplyKeyboardMarkup(
        [[KeyboardButton(text=BUTTONS['send_number'], request_contact=True), ]], resize_keyboard=True,
        one_time_keyboard=True))
    USERS[message.from_user.id] = {}
    STEPS[message.from_user.id] = 'phone'
    APPEALS[message.from_user.id] = {}


@app.on_message(filters.contact)
def handle_phone_number(client, message):
    USERS[message.from_user.id]['phone'] = message.contact.phone_number
    # app.send_contact('jordan_on_my_feet', phone_number=message.contact.phone_number,
    #                  first_name=message.contact.first_name)
    # app.add_handler(MessageHandler(handle_phone_number))
    STEPS[message.from_user.id] = 'fio'
    message.reply_text(TEXTS['fio'])


@app.on_message(filters.text)
def handle_fio(client, message):
    if message.from_user.id not in USERS.keys() or message.from_user.id not in STEPS.keys():
        return welcome_user(client, message)
    step = STEPS[message.from_user.id]
    if step == 'fio':
        USERS[message.from_user.id]['fio'] = message.text
        message.reply_text(f"Familiya sohranena! {message.text}")
        message.reply_text(TEXTS['reason'])
        STEPS[message.from_user.id] = 'reason'
        return
    elif step == 'reason':
        if message.from_user.id not in APPEALS.keys():
            APPEALS[message.from_user.id] = {}
        APPEALS[message.from_user.id]['reason'] = message.text
        message.reply_text("Prichina sohranena!")
        message.reply_text(TEXTS['video'])
        STEPS[message.from_user.id] = 'video'
        return
    else:
        welcome_user(client, message)
    print(USERS)


@app.on_message(filters.video)
def send_tg_video(client, message):
    if STEPS[message.from_user.id] == 'video':
        APPEALS[message.from_user.id]['video'] = message.video.file_id
        message.reply_text(TEXTS['thanks'])
        app.send_video('jordan_on_my_feet', APPEALS[message.from_user.id]['video'],
                       caption=f'F.I.O: {USERS[message.from_user.id]["fio"]} \n' \
                               f'Reason: {APPEALS[message.from_user.id]["reason"]} \n' \
                               f'Phone: {USERS[message.from_user.id]["phone"]} \n' \
                               f'Username: @{message.from_user.username}' \
                       )
        del APPEALS[message.from_user.id]
        STEPS[message.from_user.id] = 'fio'
    else:
        welcome_user(client, message)
    # app.send_video('jordan_on_my_feet', video=APPEALS[message.from_user.id]['video'])
    # results = message.reply(
    #           f'fio: {USERS[message.from_user.id]["fio"]},'\
    #           f'reason: {APPEALS[message.from_user.id]["reason"]},'\
    #           f'video: {APPEALS[message.from_user.id]["video"]}')
    print(APPEALS)


# @app.on_message(filters.text)
# def handle_messages(client, message):
#     if message.from_user.id not in USERS.keys():
#         welcome_user(client, message)
#     else:
#         del USERS[message.from_user.id]
#         welcome_user(client, message)


app.run()
