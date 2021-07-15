from aiogram import types


def send_languages_markup(data):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton(data['lang'][0], callback_data='lang_' + data['lang'][0]),)
    #           types.InlineKeyboardButton(data['lang'][1], callback_data='lang_' + data['lang'][1]))
    #markup.row(types.InlineKeyboardButton(data['lang'][2], callback_data='lang_' + data['lang'][2]),
    #           types.InlineKeyboardButton(data['lang'][3], callback_data='lang_' + data['lang'][3]))
    #markup.row(types.InlineKeyboardButton(data['lang'][4], callback_data='lang_' + data['lang'][4]))
    return markup


def main_menu(data, idx):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton(data['Pay'][idx], callback_data='Pay'),
               types.InlineKeyboardButton(data['Help'][idx], callback_data='Help'),
               )
    markup.row(types.InlineKeyboardButton(data['Create_a_bot'][idx], callback_data='Create_a_bot'), )
    return markup


def create_a_bot_stage_1_btn(data, idx):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.InlineKeyboardButton(data['create_a_bot_stage_1_btn'][idx], callback_data='create_a_bot_stage_1_btn'),
        types.InlineKeyboardButton(data['Back'][idx], callback_data='Back'))
    return markup


def token_info_mc(data, idx):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton(data['Change'][idx], callback_data='Change'),
               )
    markup.row(types.InlineKeyboardButton(data['Back'][idx], callback_data='Back'))
    return markup


def pay_first_mc(data, idx):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton(data['I_sent_BNB'][idx], callback_data='I_sent_BNB'))
    markup.row(types.InlineKeyboardButton(data['Back'][idx], callback_data='Back'))
    return markup


def back(data, idx):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton(data['Back'][idx], callback_data='Back'))
    return markup
