import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
about_us_text = '''Мы - команда профессионалов в сфере кредитования.\nЗа плечами наших сотрудников <b>более 7 лет банковской карьеры</b> на высоких позициях, в сфере кредитования физических юридических лиц, а так же в сфере недвижимости. Мы готовы стать для Вас верным спутником в мире финансов.'''

form_text = '''Последний шаг!\nОтправьте ваши контакты (каждый с новой строки) и мы вам перезвоним в течение 15 минут.\n\nПример:<code>\nИмя\nТелефон\nЭлектронная почта\n</code>'''

bot = telebot.TeleBot('1569999673:AAHmLXQGpLHTkh33Gs5ePQOrWMCefMABslw')

#ФУНКЦИИ
def check_data(message):
    global data
    try:
        n, p, e = message.text.split('\n')
        data[message.chat.id].append(n)
        data[message.chat.id].append(p)
        data[message.chat.id].append(e)
    except Exception:
        return False
    else:
        return True

#КЛАВИАТУРЫ
empty_k = ReplyKeyboardMarkup(resize_keyboard=True)
empty_k.add(KeyboardButton('⬅️ Вернуться назад'))

again_k = ReplyKeyboardMarkup(resize_keyboard=True)
again_k.add(KeyboardButton('🔁 Пройти ещё раз'))

p_1_k = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
p_1_k.add(KeyboardButton(' 👤 Я физическое лицо (клиент) мне нужна помощь с кредитом'), KeyboardButton(' 👥 Я юридическое лицо хочу получить финансирование'), KeyboardButton(' 🤝 Я потенциальный партнер и хочу обсудить сотрудничество'), KeyboardButton(' 🏠 Мне нужна помощь риэлтора'), KeyboardButton(' ℹ️ Расскажи сначала о себе'))

pill_blue = InlineKeyboardButton('🔵 Я отказываюсь', callback_data='pill_blue')
pill_red = InlineKeyboardButton('Попробовать 🔴', callback_data='pill_red')
pills_keyboard = InlineKeyboardMarkup(row_width=2).add(pill_blue, pill_red)

fiz_lico_k = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
fiz_lico_k.add(KeyboardButton(' 🏡 Ипотечный кредит'), KeyboardButton(' 💳 Потребительский кредит'), KeyboardButton(' 🏠 Кредит под залог недвижимости '), KeyboardButton(' 💰 Рефинансирование'), KeyboardButton(' 🏎 Автокредитование'), KeyboardButton('⬅️ Вернуться назад'))

ur_lico_k = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
ur_lico_k.add(KeyboardButton(' 🏦 Банковская гарантия'), KeyboardButton(' ⏱ Лизинг'), KeyboardButton(' 💳 Кредит'), KeyboardButton(' 💰 Проектное финансирование'), KeyboardButton('⬅️ Вернуться назад'))



#КОД
data = {}
status = {}
pills_holder = {}
@bot.message_handler(commands=['start'])
def hello_func(message):
    msg = f'''<b>Приветствую тебя!</b>\n
Хочешь найти компетентного помощника в решение твоих финансовых вопросов?
- Ты физическое лицо, и тебе необходимо получить ипотеку, потребительский кредит, кредит под залог недвижимости или быть может рефинансироваться и получить более выгодные условия по кредиту?
- Ты юридическое лицо, и ты хочешь получить Банковскую гарантию, кредитную линию или иной вид кредита?
- Ты действующий брокер или риелтор и ищешь верного партнера в решении вопросов финансирования\n
Это просто замечательно, потому что ты – избранный, <b>{message.from_user.first_name}</b>.
Может, ты ищешь меня не первый год, но я тебя искал всю жизнь!
Ну что, хочешь попробовать?\n
<i>Примешь синюю таблетку – и сказке конец.</i> Ты проснешься в своей постели и поверишь, что успешного и честного кредитного брокера не существует.
<i>Примешь красную таблетку – войдешь в страну чудес.</i> Я покажу тебе, что <b>кредиты — это выгодно и просто</b>.
'''
    pills_holder[message.chat.id] = message.message_id
    with open('./choose.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)
        status[message.chat.id] = 'first'
        bot.send_message(message.chat.id, msg, reply_markup=pills_keyboard, parse_mode='HTML')



@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('pill'))
def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    pill = callback_query.data[5:]
    bot.answer_callback_query(callback_query.id)
    if pill == 'blue':
        bot.send_message(callback_query.from_user.id, 'Ответ неверный, попробуй еще раз')
    else:
        status[callback_query.from_user.id] = 'first'
        bot.send_message(callback_query.from_user.id, 'Ты сделал правильный выбор! Расскажи о себе:', reply_markup=p_1_k)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.chat.id not in status:
        status[message.chat.id] = ''
    if 'Расскажи сначала о себе' in message.text:
        bot.send_message(message.chat.id, about_us_text, parse_mode='HTML')
        return True
    if status[message.chat.id] == 'first':
        if 'Я физическое лицо' in message.text:
            data[message.chat.id] = ['Физическое лицо']
            status[message.chat.id] = 'dop_info'
            bot.send_message(message.chat.id, 'Что бы ты хотел получить?', reply_markup=fiz_lico_k)
        elif 'Я юридическое лицо' in message.text:
            data[message.chat.id] = ['Юридическое лицо']
            status[message.chat.id] = 'dop_info'
            bot.send_message(message.chat.id, 'Что бы ты хотел получить?', reply_markup=ur_lico_k)
        elif 'партнер' in message.text:
            data[message.chat.id] = ['Партнёр', '']
            status[message.chat.id] = 'send_form'
            bot.send_message(message.chat.id, form_text, reply_markup=empty_k, parse_mode='HTML')
        elif 'помощь риэлтора' in message.text:
            data[message.chat.id] = ['Помощь Риэлтора', '']
            status[message.chat.id] = 'send_form'
            bot.send_message(message.chat.id, form_text, reply_markup=empty_k, parse_mode='HTML')
    elif status[message.chat.id] == 'dop_info':
        if 'назад' in message.text:
            status[message.chat.id] = 'first'
            bot.send_message(message.chat.id, 'Расскажи о себе', reply_markup=p_1_k)
            return 1
        data[message.chat.id].append(message.text)
        status[message.chat.id] = 'send_form'
        bot.send_message(message.chat.id, form_text, reply_markup=empty_k, parse_mode='HTML')
    elif status[message.chat.id] == 'send_form':
        if 'назад' in message.text:
            if data[message.chat.id][0] == 'Партнёр' or data[message.chat.id][0] == 'Помощь Риэлтора':
                status[message.chat.id] = 'first'
                data[message.chat.id].pop()
                bot.send_message(message.chat.id, 'Расскажи о себе', reply_markup=p_1_k)
            elif data[message.chat.id][0] == 'Физическое лицо':
                status[message.chat.id] = 'dop_info'
                data[message.chat.id].pop()
                bot.send_message(message.chat.id, 'Что бы ты хотел получить?', reply_markup=fiz_lico_k)
            elif data[message.chat.id][0] == 'Юридическое лицо':
                status[message.chat.id] = 'dop_info'
                bot.send_message(message.chat.id, 'Что бы ты хотел получить?', reply_markup=ur_lico_k)
            return 1

        if check_data(message):
            status[message.chat.id] = 'finished'
            bot.send_message(message.chat.id, 'Спасибо! Ваша заявка успешно подана!', reply_markup=again_k)
            bot.send_message('@mortgagca', f"👨‍💻Новая заявка!\nТип: {data[message.chat.id][0] + ' ' + data[message.chat.id][1]}\nИмя: {data[message.chat.id][2]}\nТелефон: {data[message.chat.id][3]}\nЭл.почта: {data[message.chat.id][4]}" ,parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Проверьте корректность введёных данных')
    elif status[message.chat.id] == 'finished':
        if 'Пройти ещё раз' in message.text:
            status[message.chat.id] = 'first'
            bot.send_message(message.chat.id, 'Привет, расскажи сначала о себе!', reply_markup=p_1_k)
        else:
            bot.send_message(message.chat.id, 'Ты уже отправил заявку. Скоро мы тебе позвоним. Если хочешь пройти ещё раз - нажми на кнопку снизу.')





bot.polling(none_stop=True, interval=0)