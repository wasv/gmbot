from gmbot import Dispatcher
import fileinput

try:
    input = raw_input
except NameError:
    pass

d = Dispatcher()

while True:
    line = input()
    print(d.dispatch('cli','cli',line))
