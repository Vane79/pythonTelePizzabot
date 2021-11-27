from transitions import Machine


class PizzaBot(object):
    states = \
        [
            'sleep',
            'asking_size',
            'asking_payment',
            'acknowledging',
        ]

    transitions = \
        [
            {'trigger': 'wakeup', 'source': '*', 'dest': 'asking_size'},
            {'trigger': 'ask_payment', 'source': 'asking_size', 'dest': 'asking_payment'},
            {'trigger': 'received_payment_info', 'source': 'asking_payment', 'dest': 'acknowledging'},
            {'trigger': 'stop', 'source': '*', 'dest': 'sleep', 'after': 'stop_message'},

        ]

    def __init__(self):
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial='sleep')
        self.size = None
        self.payment = None

    def ask_for_size(self):
        return 'Какую пиццу Вы хотите?'

    def ask_for_pay(self):
        return 'Чем Вы будете платить?'

    def confirmation(self):
        return f"Вы хотите {self.size} пиццу, а оплата {self.payment}?"

    def thank_you(self):
        return f"Спасибо за заказ"

    def stop_message(self):
        return "Напишите /start чтобы попробовать снова"
