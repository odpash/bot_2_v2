from markups import send_languages_markup, main_menu, create_a_bot_stage_1_btn, token_info_mc
from database_editing import get_lang, registration_user_in_db, read_records_from_db, change_user_param_in_db
from markups import pay_first_mc, back
from database_editing import add_record_to_db


def is_combo_true(trans, wallet):
    if trans == '12345' and wallet == '54321':
        return True
    else:
        return False


def answer_edit_message(bot, call, text, menu=None, callback=''):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=text,
                              message_id=call.message.message_id,
                              reply_markup=[menu],
                              parse_mode='HTML')
    except:
        pass
    bot.answer_callback_query(callback_query_id=call.id, text=callback)


def send_languages(bot, message, data):
    markup = send_languages_markup(data)
    answer = data['start_info']
    bot.send_message(message.chat.id, answer, reply_markup=[markup])


def send_languages_cb(bot, callback, data):
    callback.data = callback.data.replace('lang_', '')
    if callback.data != data['lang'][0]:  # if not English
        answer_edit_message(bot, callback, data['only_eng'][0] + '\n\n' + data['start_info'][0],
                            send_languages_markup(data))
    else:
        registration_user_in_db(callback.from_user.id, callback.data)
        bot.answer_callback_query(callback.id)
        send_main_menu(bot, callback, data)
        pass  # Here we are going to the pay stage


def send_main_menu(bot, callback, data):
    lang_idx = get_lang(callback.from_user.id, data)
    answer = data['main_menu'][lang_idx]
    markup = main_menu(data, lang_idx)
    answer_edit_message(bot, callback, answer, markup)


def create_a_bot_stage_1(bot, callback, data):
    _, hash_info, _, _ = read_records_from_db(callback.from_user.id)
    lang_idx = get_lang(callback.from_user.id, data)
    if hash_info == 'None' or hash_info == 'editing':
        answer = data['create_a_bot_stage_1_text'][int(lang_idx)]
        markup = create_a_bot_stage_1_btn(data, int(lang_idx))
        answer_edit_message(bot, callback, answer, markup)
    else:
        create_a_bot_stage_info(bot, callback, data, 1)


def create_a_bot_stage_edit(bot, callback, data):  # --
    lang_idx = get_lang(callback.from_user.id, data)
    answer = data['enter_token'][lang_idx]
    answer_edit_message(bot, callback, answer)
    change_user_param_in_db(callback.from_user.id, 'editing', 'hash')


def create_a_bot_stage_info(bot, callback, data, from_what):
    lang_idx = get_lang(callback.from_user.id, data)
    markup = token_info_mc(data, lang_idx)
    _, user_token, _, _ = read_records_from_db(callback.from_user.id)
    if from_what == 2:
        answer = data['token_success_edit'][lang_idx] + '\n\n' + data['token_info'][lang_idx] + user_token
        bot.send_message(callback.chat.id, answer, reply_markup=[markup])
    else:
        answer = data['token_info'][lang_idx] + user_token
        callback.message.chat.id = callback.from_user.id
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=answer,
                              reply_markup=[markup])
        bot.answer_callback_query(callback.id)


def help_stage(bot, callback, data):
    lang_idx = get_lang(callback.from_user.id, data)
    answer = data['help_text'][lang_idx]
    markup = back(data, lang_idx)
    answer_edit_message(bot, callback, answer, markup)


def pay_first_stage(bot, callback, data):
    lang_idx = get_lang(callback.from_user.id, data)
    answer = data['Send_BNB_to_the_adress'][lang_idx]
    markup = pay_first_mc(data, lang_idx)
    answer_edit_message(bot, callback, answer, markup)


def pay_second_stage(bot, callback, data, rz):
    lang_idx = get_lang(callback.from_user.id, data)
    answer = data['Enter_trans'][lang_idx]
    if rz == 2:
        bot.send_message(callback.chat.id, answer)
    else:
        bot.send_message(callback.message.chat.id, answer)
    change_user_param_in_db(callback.from_user.id, 'editing', 'last_trans')


def pay_third_stage(bot, callback, data):
    lang_idx = get_lang(callback.from_user.id, data)
    answer = data['Enter_wallet'][lang_idx]
    bot.send_message(callback.chat.id, answer)
    change_user_param_in_db(callback.from_user.id, 'editing', 'last_wallet')


def pay_last_stage(bot, callback, data):
    _, hash_info, trans, wallet = read_records_from_db(callback.from_user.id)
    lang_idx = get_lang(callback.from_user.id, data)
    markup = back(data, lang_idx)
    if is_combo_true(trans, wallet):
        answer = data['Tr_ok'][lang_idx]
        add_record_to_db(callback.from_user.id, trans, wallet)
    else:
        answer = data['Tr_error'][lang_idx]
    bot.send_message(callback.chat.id, answer, reply_markup=[markup])
