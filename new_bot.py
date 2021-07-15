import re

import telebot
from database_editing import parse_txt_file, read_records_from_db, change_user_param_in_db, get_lang
from new_steps import send_languages, send_languages_cb, create_a_bot_stage_1, help_stage, create_a_bot_stage_edit
from aiogram import types
from new_steps import create_a_bot_stage_info, send_main_menu, pay_first_stage, pay_second_stage, pay_third_stage
from new_steps import pay_last_stage


def check_wallet(a):
    if re.search(r'0x[a-fA-F0-9]{40}', a) is not None:
        return True
    return False


def check_trans(a):
    if re.search(r'0x[a-fA-F0-9]{64}', a) is not None:
        return True
    return False


token = '1712170001:AAE3r4S9o5R7jtI092xaJSMai_TcY3fb4OY'
bot = telebot.TeleBot(token)
data = parse_txt_file('config_bot_2.txt')


@bot.callback_query_handler(func=lambda c: 'lang' in c.data)
def send_languages_callback(callback_query: types.CallbackQuery):
    send_languages_cb(bot, callback_query, data)


@bot.callback_query_handler(func=lambda c: 'Create_a_bot' in c.data)
def create_a_bot_stage_1_cb(callback_query: types.CallbackQuery):
    create_a_bot_stage_1(bot, callback_query, data)


@bot.callback_query_handler(func=lambda c: 'Help' in c.data)
def help_cb(callback_query: types.CallbackQuery):
    help_stage(bot, callback_query, data)


@bot.callback_query_handler(func=lambda c: 'create_a_bot_stage_1_btn' in c.data or 'Change' in c.data)
def edit_cb(callback_query: types.CallbackQuery):
    create_a_bot_stage_edit(bot, callback_query, data)


@bot.callback_query_handler(func=lambda c: 'Back' in c.data)
def send_main_menu_cb(callback_query: types.CallbackQuery):
    send_main_menu(bot, callback_query, data)


@bot.callback_query_handler(func=lambda c: 'Pay' in c.data)
def pay_cb(callback_query: types.CallbackQuery):
    pay_first_stage(bot, callback_query, data)


@bot.callback_query_handler(func=lambda c: 'I_sent_BNB' in c.data)
def pay_2_cb(callback_query: types.CallbackQuery):
    pay_second_stage(bot, callback_query, data, 1)


@bot.message_handler()
def initialize(message):
    print(message.text, message.from_user.id)
    if message.text == '/start':
        send_languages(bot, message, data)
    else:
        _, hash_info, trans, wallet = read_records_from_db(message.from_user.id)
        lang = get_lang(message.from_user.id, data)
        if hash_info == 'editing':
            change_user_param_in_db(message.from_user.id, message.text, 'hash')
            create_a_bot_stage_info(bot, message, data, 2)
        elif trans == 'editing':
            if check_trans(message.text):
                change_user_param_in_db(message.from_user.id, message.text, 'last_trans')
                pay_third_stage(bot, message, data)
            else:
                bot.send_message(message.chat.id, data['error_trans'][lang])
                pay_second_stage(bot, message, data, 2)
        elif wallet == 'editing':
            if check_wallet(message.text):
                change_user_param_in_db(message.from_user.id, message.text, 'last_wallet')
                pay_last_stage(bot, message, data)
            else:
                bot.send_message(message.chat.id, data['error_wallet'][lang])
                pay_third_stage(bot, message, data)
        else:
            bot.send_message(message.chat.id, 'Unknown command. Please write /start.')


bot.polling(none_stop=True)
