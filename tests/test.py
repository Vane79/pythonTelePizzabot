import pytest
from bot.bones import PizzaBot

states = \
    [
        'sleep',
        'asking_size',
        'asking_payment',
        'acknowledging',
    ]


@pytest.fixture()
def instance():
    test_instance = PizzaBot()
    return test_instance


def test(instance):
    i = 0
    while i != len(states):
        assert instance.state == states[i]
        instance.next_state()
        i += 1
