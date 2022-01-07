import Pakano
from Pakano import *

# to run, type:
# py -m pytest TestPakano.py -vvv

# test class:
class TestClass():
    def test_get_cpu_move(self):
        for i in range(10):
            assert get_cpu_move() in list('pkn')


    def test_repeat_or_not_true(self):
        Pakano.input = lambda x: 'T'
        output = repeat_or_not()
        assert output == True


# ...or separate functions tests:
def test_repeat_or_not_false():
    for i in list('qweryuiopasdfghjkzxcvbnm'):
        Pakano.input = lambda x: 'i'
        output = repeat_or_not()
        assert output == None

def test_fight():
    p, k, n = tuple("pkn")

    assert fight(p, k) == -1
    assert fight(p, p) == 0
    assert fight(p, n) == 1



# print(test_repeat_or_not())