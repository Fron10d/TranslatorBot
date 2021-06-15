# Libs
from bot import config
import telebot
from google.cloud import translate_v2
from gtts import gTTS
import os
import time

# TOKEN
bot = telebot.TeleBot('TOKEN')
mydb = config.mydb

# API
os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = r''

# глобальные переменные
glob_lang = 'en'
target = 'en'
langs = ['en', 'kk', 'ru']

# -----------Клавиатура уроков--------------
lessons = telebot.types.InlineKeyboardMarkup()

lessons.row(
    telebot.types.InlineKeyboardButton('Урок номер 1', url='https://lingust.ru/english/grammar/lesson1')
)

lessons.row(
    telebot.types.InlineKeyboardButton('Урок номер 2', url='https://lingust.ru/english/grammar/lesson2'),
    telebot.types.InlineKeyboardButton('Урок номер 3', url='https://lingust.ru/english/grammar/lesson3'),
)

lessons.row(
    telebot.types.InlineKeyboardButton('Урок номер 4', url='https://lingust.ru/english/grammar/lesson4'),
    telebot.types.InlineKeyboardButton('Урок номер 5', url='https://lingust.ru/english/grammar/lesson5'),
)
lessons.row(
    telebot.types.InlineKeyboardButton('Урок номер 6', url='https://lingust.ru/english/grammar/lesson6'),
    telebot.types.InlineKeyboardButton('Урок номер 7', url='https://lingust.ru/english/grammar/lesson7'),
)

lessons.row(
    telebot.types.InlineKeyboardButton('Урок номер 8', url='https://lingust.ru/english/grammar/lesson8'),
    telebot.types.InlineKeyboardButton('Урок номер 9', url='https://lingust.ru/english/grammar/lesson9'),
)
lessons.row(
    telebot.types.InlineKeyboardButton('Урок номер 10', url='https://lingust.ru/english/grammar/lesson10'),
    telebot.types.InlineKeyboardButton('Урок номер 11', url='https://lingust.ru/english/grammar/lesson11'),
)
lessons.row(
    telebot.types.InlineKeyboardButton('Урок 12', url='https://lingust.ru/english/grammar/lesson12'),
    telebot.types.InlineKeyboardButton('Урок 13', url='https://lingust.ru/english/grammar/lesson13'),
    telebot.types.InlineKeyboardButton('Урок 14', url='https://lingust.ru/english/grammar/lesson14')
)


# start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Это бот-переводчик.\n' +
        'Бот умеет переводить на три языка\n(English, Kazakh, Russian, Ukrainan, Uzbek, Kyrgyz, Turkmen, Azerbaijani etc.).'
        'По умолчанию бот переводит на английский\n'
        'Чтобы сменить язык, нажмите на /change.\n' +
        'Для справки, нажмите на /help.\n'
        'Для регистрации /registration'
    )


# registration in DB
@bot.message_handler(commands=['registration'])
def start_command(message):
    mycursor = mydb.cursor()  # special object that makes requests and receives their results
    sql = "SELECT * FROM users WHERE id = %s"
    adr = (str(message.from_user.id),)
    mycursor.execute(sql, adr, )
    myresult = mycursor.fetchall()
    if myresult is None or myresult == [] or myresult == ():
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (id) VALUES (%s)"
        val = (str(message.from_user.id),)
        mycursor.execute(sql, val)  # makes an INSERT query against the database using normal SQL syntax
        mydb.commit()  # when we make changes to the database - 'commit()' saves the transaction
        bot.reply_to(message, "Поздравляем," + " " + (str(message.from_user.first_name)) + ", Вы зарегистрированы")
    else:
        bot.reply_to(message, (
            str(message.from_user.first_name)) + ", Вы  уже зарегистрированы! Можете приступать к переводу)  ")


# last user translates
@bot.message_handler(commands=['mytranslates'])
def rows_command(message):
    try:
        mycursor_2 = mydb.cursor()  # special object that makes requests and receives their results
        sql_2 = "SELECT translated_text FROM  users WHERE id = %s"
        adr_2 = (str(message.from_user.id),)
        mycursor_2.execute(sql_2, adr_2, )
        rows = mycursor_2.fetchall()
        for row in rows:
            print(row)

        bot.reply_to(message, "" + "@" + (message.from_user.username) + " Ваш послдений перевод:" + "\n" + str(row))
    # except Error as e:
    #         print(e)
    finally:
        mycursor_2.close()


#   help
@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message to developer', url="https://t.me/@maksutovm"
        )
    )
    bot.send_message(
        message.chat.id,
        '1) Этот бот переводчик.\n' +
        '2) Проект находится в бэта тестировании.\n' +
        '3) Если у вас есть какие-либо замечания или предложения, вы можете связаться с разработчиком по ссылке ниже.',
        reply_markup=keyboard
    )


# text to audio
@bot.message_handler(commands=['audio'])
def send_audio(message):
    try:
        if hasattr(message.reply_to_message, 'text'):
            file_name = f'{str(message.chat.id)}.ogg'
            tts = gTTS(message.reply_to_message.text, lang=target)
            tts.save(file_name)
            with open(file_name, 'rb') as voice_message:
                bot.send_voice(chat_id=message.chat.id, voice=voice_message)
            os.remove(file_name)
        else:
            bot.send_message(message.chat.id, 'Ответьте на сообщение используя эту комманду')
    except:
        audio_error = 'К сожалению у этого языка нету аудиоподдержки, попробуйте выбрать русский или английский'
        bot.send_message(message.chat.id, audio_error)
        print('error')


# English grammar
@bot.message_handler(commands=['grammar'])
def send_grammar(message):
    link_button = telebot.types.InlineKeyboardMarkup()
    link_button.row(
        telebot.types.InlineKeyboardButton('Смотреть', callback_data='view')
    )

    text = '<b>Грамматика английского языка</b>\nОнлайн справочник грамматики английского языка с подробным ' \
           'изложением особенностей употребления частей речи, а также построения английских предложений. '

    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=link_button)


# callback func grammar
@bot.callback_query_handler(func=lambda call: call.data == 'view')
def grammar_callback(query: telebot.types.CallbackQuery):
    data = query.data
    if data == 'view':
        bot.edit_message_text('Выберете урок', message_id=query.message.message_id, chat_id=query.message.chat.id,
                              reply_markup=lessons)


# Change language
@bot.message_handler(commands=['change'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('🇰🇿 Kazakh ', callback_data='get-kk')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇷🇺 Russian ', callback_data='get-ru')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇺🇦 Ukrainan ', callback_data='get-uk')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇬🇧 English ', callback_data='get-en')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇺🇿 Uzbek ', callback_data='get-uz')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇰🇬 Kyrgyz ', callback_data='get-ky')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇹🇲 Turkmen ', callback_data='get-tk')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇦🇿 Azerbaijani ', callback_data='get-az')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇹🇼 Chinese ', callback_data='get-zh-TW')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇪🇸 Spanish ', callback_data='get-es')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇮🇳 Hindi ', callback_data='get-hi')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇵🇹 Portuguese ', callback_data='get-pt')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇯🇵 Japanese ', callback_data='get-ja')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇩🇪 German ', callback_data='get-de')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇰🇷 Korean ', callback_data='get-ko')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇹🇷 Turkish', callback_data='get-tr')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇦🇪 Arabic', callback_data='get-ar')
    ),

    keyboard.row(
        telebot.types.InlineKeyboardButton('🇮🇹 Italian', callback_data='get-it')
    )

    bot.send_message(
        message.chat.id,
        'Выберите на какой язык перевести (текст для перевода может быть на любом языке, бот определит, на каком языке вы пишите и переведет на нужный):',
        reply_markup=keyboard
    )


# keyboard
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)


def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:])


#
def send_exchange_result(message, ex_code):
    bot.send_chat_action(message.chat.id, 'typing')
    global target
    target = ex_code
    bot.send_message(
        message.chat.id, "Target language changed to " + ex_code.title()
    )


# translate
@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text'])
def send_text(message):
    try:
        translate_client = translate_v2.Client()
        global target
        text = message.text
        result = translate_client.translate(
            text,
            target_language=target)
        output = translate_client.translate(
            text,
            target_language=target)
        print(format(result["translatedText"]))
        print(output)
        # tts = gTTS(text=text, lang='ru')
        # tts.save('sound.mp3')
        error = 'Извините, произошла ошибка, попробуйте заново, возможно в тексте были неопознанные символы или было переслано сразу несколько сообщений'
        bot.send_message(message.chat.id, output['translatedText'])

        mycursor = mydb.cursor()  # special object that makes requests and receives their results
        sql = "SELECT * FROM users WHERE translated_text = %s"
        adr = (str(message.text),)
        mycursor.execute(sql, adr, )
        myresult = mycursor.fetchall()  # gets the result of the request made
        if myresult is None or myresult == [] or myresult == ():
            mycursor = mydb.cursor()
            sql = "INSERT INTO users (id, username, translated_text, input_text, language) VALUES (%s, %s, %s, %s, %s)"
            val = (str(message.from_user.id), (str(message.from_user.username)), (format(result["translatedText"])),
                   (format(result["input"])), (format(result["detectedSourceLanguage"])))
            mycursor.execute(sql, val)  # makes an INSERT query against the database using normal SQL syntax
            mydb.commit()  # when we make changes to the database - 'commit()' saves the transaction
    except:
        # bot.send_message(message.chat.id, error)
        pass


# work in the group
@bot.message_handler(func=lambda message: message.chat.type == 'group' and message.entities is not None)
def send_text_in_group(message):
    if '#en' in message.text:
        translate_client = translate_v2.Client()
        text_1 = message.reply_to_message.text
        output = translate_client.translate(
            text_1,
            target_language=langs[0])
        print(output)
        bot.send_message(message.chat.id, output['translatedText'])

    elif '#kk' in message.text:
        translate_client = translate_v2.Client()
        text_2 = message.reply_to_message.text
        output = translate_client.translate(
            text_2,
            target_language=langs[1])
        print(output)
        bot.send_message(message.chat.id, output['translatedText'])

    elif '#ru' in message.text:
        translate_client = translate_v2.Client()
        text_3 = message.reply_to_message.text
        output = translate_client.translate(
            text_3,
            target_language=langs[2])
        print(output)
        bot.send_message(message.chat.id, output['translatedText'])


# run
while True:
    try:
        bot.polling(none_stop=True)

    except Exception as exs:
        print(exs)

        time.sleep(15)
