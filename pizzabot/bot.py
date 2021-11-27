import bones
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from teletoken import key

bot = telebot.TeleBot(key, parse_mode=None)
talker = bones.PizzaBot()

size_markup = ReplyKeyboardMarkup()
sml_p = KeyboardButton('Маленькую')
med_p = KeyboardButton('Среднюю')
big_p = KeyboardButton('Большую')
size_markup.row(sml_p, med_p, big_p)

payment_markup = ReplyKeyboardMarkup()
cash = KeyboardButton('Наличными')
card = KeyboardButton('Картой')
payment_markup.row(card, cash)

y_n_markup = ReplyKeyboardMarkup()
yes = KeyboardButton('Да')
no = KeyboardButton('Нет')
y_n_markup.row(yes, no)


@bot.message_handler(commands='start')
def wake(message):
    talker.client = message.chat.first_name
    bot.send_message(message.chat.id, talker.ask_for_size(), reply_markup=size_markup)
    talker.wakeup()


@bot.message_handler(commands='stop')
def come_again(message):
    bot.send_message(message.chat.id, talker.stop_message())
    talker.stop()


@bot.message_handler(content_types='text')
def talking(message):
    if talker.state == 'asking_size' and message.text.lower() in ('маленькую', 'среднюю', 'большую'):
        talker.size = message.text.lower()
        bot.send_message(message.chat.id, talker.ask_for_pay(), reply_markup=payment_markup)
        talker.ask_payment()
    elif talker.state == 'asking_payment' and message.text.lower() in ('наличными', 'картой'):
        talker.payment = message.text.lower()
        talker.received_payment_info()
        bot.send_message(message.chat.id, talker.confirmation(), reply_markup=y_n_markup)
    elif talker.state == 'acknowledging' and message.text.lower() == 'да':
        bot.send_message(message.chat.id, talker.thank_you(), reply_markup=ReplyKeyboardRemove())
        talker.stop()
        save_order(message.chat.first_name, message.chat.last_name, talker.size, talker.payment)
    elif talker.state == 'acknowledging' and message.text.lower() == 'нет':
        bot.send_message(message.chat.id, talker.stop_message(), reply_markup=ReplyKeyboardRemove())
        talker.stop()


def save_order(client_name, client_surname, size, payment):
    file = open('orders.txt', 'a')
    file.write(f'{size} пиццу для {client_name} {client_surname}, оплата {payment}\n')
    file.close()


if __name__ == '__main__':
    bot.polling()
