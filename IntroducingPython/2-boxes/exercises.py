#!/usr/bin/env python3

'''Глава 5. Py Boxes: модули, пакеты и программы'''

'''1. Создайте файл, который называется zoo.py. В нем объявите функцию hours(), которая выводит на экран строку 
' Open 9-5 daily'. Далее используйте интерактивный интерпретатор, чтобы импортировать модуль zoo и вызвать его 
функцию hours().'''

import zoo
zoo.hours()

print('\n================================ RESTART ================================\n')

'''2. В интерактивном интерпретаторе импортируйте модуль zoo под именем menagerie и вызовите его функцию hours().'''

import zoo as menagerie
menagerie.hours()

print('\n================================ RESTART ================================\n')

'''3. Оставаясь в интерпретаторе, импортируйте непосредственно функцию hours() из модуля zoo и вызовите ее.'''

from zoo import hours
hours()

print('\n================================ RESTART ================================\n')

'''4. Импортируйте функцию hours() под именем info и вызовите ее.'''

from zoo import hours as info
info()

print('\n================================ RESTART ================================\n')

'''5. Создайте словарь с именем plain, содержащий пары «ключ — значение» 'a': 1, 'b': 2 и 'c':3, 
а затем выведите его на экран.'''

plain = {'a': 1, 'b': 2, 'c': 3}
print(plain)

print('\n================================ RESTART ================================\n')

'''6. Создайте OrderedDict с именем fancy из пар «ключ — значение», приведенных в упражнении 5, 
и выведите его на экран. Изменился ли порядок ключей?'''

from collections import OrderedDict
fancy = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(fancy)

print('\n================================ RESTART ================================\n')

'''7. Создайте defaultdict с именем dict_of_lists и передайте ему аргумент list. 
Создайте список dict_of_lists['a'] и присоедините к нему значение 'something for a' за одну операцию. 
Выведите на экран dict_of_lists['a'].'''

from collections import defaultdict
dict_of_lists = defaultdict(list)
dict_of_lists['a'].append('something for a')
print(dict_of_lists['a'])

print('\n================================ RESTART ================================\n')

'''Глава 6. Ой-ой-ой: объекты и классы'''

'''1. Создайте класс, который называется Thing, не имеющий содержимого, и выведите его на экран. 
Затем создайте объект example этого класса и также выведите его. Совпадают ли выведенные значения?'''

class Thing:
    pass
print(Thing)

example = Thing()
print(example)

print('\n================================ RESTART ================================\n')

'''2. Создайте новый класс с именем Thing2 и присвойте его атрибуту letters значение 'abc'. 
Выведите на экран значение атрибута letters.'''

class Thing2:
    letters = 'abc'

print(Thing2.letters)

print('\n================================ RESTART ================================\n')

'''3. Создайте еще один класс, который, конечно же, называется Thing3. В этот раз присвойте значение 'xyz' 
атрибуту объекта, который называется letters. Выведите на экран значение атрибута letters. Понадобилось ли вам 
создавать объект класса, чтобы сделать это?'''

class Thing3:
    def __init__(self):
        self.letters = 'xyz'

something = Thing3()
print(something.letters)

print('\n================================ RESTART ================================\n')

'''4. Создайте класс, который называется Element, имеющий атрибуты объекта name, symbol и number. 
Создайте объект этого класса со значениями 'Hydrogen', 'H' и 1.'''

class Element():
    def __init__(self, name, symbol, number):
        self.name = name
        self.symbol = symbol
        self.number = number

hydrogen = Element('Hydrogen', 'H', '1')
print(hydrogen.name, hydrogen.symbol, hydrogen.number)

print('\n================================ RESTART ================================\n')

'''5. Создайте словарь со следующими ключами и значениями: 'name': 'Hydrogen', 'symbol': 'H', 'number': 1. 
Далее создайте объект с именем hydrogen класса Element с помощью этого словаря.'''

el_dict = {'name': 'Hydrogen', 'symbol': 'H', 'number': 1}
print(el_dict)

hydrogen = Element(el_dict['name'], el_dict['symbol'], el_dict['number'])
print(hydrogen.name, hydrogen.symbol, hydrogen.number)

hydrogen = Element(**el_dict)
print(hydrogen.name, hydrogen.symbol, hydrogen.number)

print('\n================================ RESTART ================================\n')

'''6. Для класса Element определите метод с именем dump(), который выводит на экран значения атрибутов объекта 
(name, symbol и number). Создайте объект hydrogen из этого нового определения и используйте метод dump(), 
чтобы вывести на экран его атрибуты.'''

class Element:
    def __init__(self, name, symbol, number):
        self.name = name
        self.symbol = symbol
        self.number = number
    def dump(self):
        print('name=%s, symbol=%s, number=%s' % (self.name, self.symbol, self.number))

hydrogen = Element(**el_dict)
print(hydrogen.dump())

print('\n================================ RESTART ================================\n')

'''7. Вызовите функцию print(hydrogen). В определении класса Element измените имя метода dump на __str__, 
создайте новый объект hydrogen и затем снова вызовите метод print(hydrogen).'''

print(hydrogen)

class Element:
    def __init__(self, name, symbol, number):
        self.name = name
        self.symbol = symbol
        self.number = number
    def __str__(self):
        return ('name=%s, symbol=%s, number=%s' % (self.name, self.symbol, self.number))

hydrogen = Element(**el_dict)
print(hydrogen)

print('\n================================ RESTART ================================\n')

'''8. Модифицируйте класс Element, сделав атрибуты name, symbol и number закрытыми. 
Определите для каждого атрибута свойство получателя, возвращающее значение соответствующего атрибута.'''

class Element:
    def __init__(self, name, symbol, number):
        self.__name = name
        self.__symbol = symbol
        self.__number = number
    @property
    def name(self):
        return self.__name
    @property
    def symbol(self):
        return self.__symbol
    @property
    def number(self):
        return self.__number

hydrogen = Element('Hydrogen', 'H', '1')

print(hydrogen.name)
print(hydrogen.symbol)
print(hydrogen.number)

print('\n================================ RESTART ================================\n')

'''9. Определите три класса: Bear, Rabbit и Octothorpe. Для каждого из них определите всего один метод — eats(). 
Он должен возвращать значения 'berries' (для Bear), 'clover' (для Rabbit) или 'campers' (для Octothorpe). 
Создайте по одному объекту каждого класса и выведите на экран то, что ест указанное животное.'''

class Bear:
    def eats(self):
        return 'berries'

class Rabbit:
    def eats(self):
        return 'clover'

class Octothorpe:
    def eats(self):
        return 'campers'

b = Bear()
r = Rabbit()
o = Octothorpe()

print(b.eats())
print(r.eats())
print(o.eats())

print('\n================================ RESTART ================================\n')

'''10. Определите три класса: Laser, Claw и SmartPhone. Каждый из них имеет только один метод — does(). 
Он возвращает значения 'disintegrate' (для Laser), 'crush' (для Claw) или 'ring' (для SmartPhone). 
Далее определите класс Robot, который содержит по одному объекту каждого из этих классов. 
Определите метод does() для класса Robot, который выводит на экран все, что делают его компоненты.'''

class Laser:
    def does(self):
        return 'disintegrate'
    
class Claw:
    def does(self):
        return 'crush'
    
class SmartPhone:
    def does(self):
        return 'ring'

class Robot:
    def __init__(self):
        self.laser = Laser()
        self.claw = Claw()
        self.smartphone = SmartPhone()
    def does(self):
        return '''I have many attachments:
        My laser, to %s.
        My claw, to %s.
        My smartphone, to %s.''' % (
            self.laser.does(),
            self.claw.does(),
            self.smartphone.does())

robbie = Robot()
print(robbie.does())

print('\n================================ RESTART ================================\n')

'''Глава 7. Работаем с данными профессионально'''

'''1. Создайте строку Unicode с именем mystery и присвойте ей значение '\U0001f4a9'. 
Выведите на экран значение строки mystery. Найдите имя Unicode для mystery.'''

import unicodedata

mystery = '\U0001f4a9'
print(mystery)

print(unicodedata.name(mystery))

print('\n================================ RESTART ================================\n')

'''2. Закодируйте строку mystery, в этот раз с использованием кодировки UTF-8, 
в переменную типа bytes с именем pop_bytes. Выведите на экран значение переменной pop_bytes.'''

pop_bytes = mystery.encode('utf-8')
print(type(pop_bytes))
print(pop_bytes)

print('\n================================ RESTART ================================\n')

'''3. Используя кодировку UTF-8, декодируйте переменную pop_bytes в строку pop_string. 
Выведите на экран значение переменной pop_string. Равно ли оно значению переменной mystery?'''

pop_string = pop_bytes.decode('utf-8')
print(type(pop_string))
print(pop_string)
print(pop_string == mystery)

print('\n================================ RESTART ================================\n')

'''4. Запишите следующее стихотворение с помощью старого стиля форматирования. 
Подставьте строки 'roast beef', 'ham', 'head' и 'clam' в эту строку:
My kitty cat likes %s,
My kitty cat likes %s,
My kitty cat fell on his %s
And now thinks he's a %s.'''

poem = '''
    My kitty cat likes %s,
    My kitty cat likes %s,
    My kitty cat fell on his %s
    And now thinks he's a %s.
    '''
args = ('roast beef', 'ham', 'head', 'clam')
print(poem % args)

print('\n================================ RESTART ================================\n')

'''5. Запишите следующее письмо по форме с помощью форматирования нового стиля. 
Сохраните строку под именем letter (это имя вы используете в следующем упражнении):
Dear {salutation} {name},
Thank you for your letter. We are sorry that our {product} {verbed} in your
{room}. Please note that it should never be used in a {room}, especially
near any {animals}.
Send us your receipt and {amount} for shipping and handling. We will send
you another {product} that, in our tests, is {percent}% less likely to
have {verbed}.
Thank you for your support.
Sincerely,
{spokesman}
{job_title}'''

letter = '''
    Dear {salutation} {name},
    
    Thank you for your letter. We are sorry that our {product} {verbed} in your
    {room}. Please note that it should never be used in a {room}, especially
    near any {animals}.
    
    Send us your receipt and {amount} for shipping and handling. We will send
    you another {product} that, in our tests, is {percent}% less likely to
    have {verbed}.
    
    Thank you for your support.
    
    Sincerely,
    {spokesman}
    {job_title}
    '''

print(letter)

print('\n================================ RESTART ================================\n')

'''6. Создайте словарь с именем response, имеющий значения для строковых ключей 'salutation', 'name', 'product', 
'verbed' (прошедшее время от глагола verb), 'room', 'animals', 'amount', 'percent', 'spokesman' и 'job_title'. 
Выведите на экран значение переменной letter, в которую подставлены значения из словаря response.'''

response = {
    'salutation': 'Colonel',
    'name': 'Hackenbush',
    'product': 'duck blind',
    'verbed': 'imploded',
    'room': 'conservatory',
    'animals': 'emus',
    'amount': '$1.38',
    'percent': '1',
    'spokesman': 'Edgar Schmeltz',
    'job_title': 'Licensed Podiatrist'
    }

print(letter.format(**response))

print('\n================================ RESTART ================================\n')

'''7. При работе с текстом вам могут пригодиться регулярные выражения. 
Мы воспользуемся ими несколькими способами в следующем примере текста. 
Перед вами стихотворение Ode on the Mammoth Cheese, написанное Джеймсом Макинтайром (James McIntyre) в 1866 году 
во славу головки сыра весом 7000 фунтов, которая была сделана в Онтарио и отправлена в международное путешествие. 
Если не хотите вводить это стихотворение целиком, используйте свой любимый поисковик и скопируйте его текст в 
программу. Или скопируйте его из проекта «Гутенберг» (http://bit.ly/mcintyre-poetry). 
Назовите следующую строку mammoth:

We have seen thee, queen of cheese,
Lying quietly at your ease,
Gently fanned by evening breeze,
Thy fair form no flies dare seize.
All gaily dressed soon you'll go
To the great Provincial show,
To be admired by many a beau
In the city of Toronto.
Cows numerous as a swarm of bees,
Or as the leaves upon the trees,
It did require to make thee please,
And stand unrivalled, queen of cheese.
May you not receive a scar as
We have heard that Mr. Harris
Intends to send you off as far as
The great world's show at Paris.
Of the youth beware of these,
For some of them might rudely squeeze
And bite your cheek, then songs or glees
We could not sing, oh! queen of cheese.
We'rt thou suspended from balloon,
You'd cast a shade even at noon,
Folks would think it was the moon
About to fall and crush them soon.'''

mammoth = '''
We have seen thee, queen of cheese,
Lying quietly at your ease,
Gently fanned by evening breeze,
Thy fair form no flies dare seize.
All gaily dressed soon you'll go
To the great Provincial show,
To be admired by many a beau
In the city of Toronto.
Cows numerous as a swarm of bees,
Or as the leaves upon the trees,
It did require to make thee please,
And stand unrivalled, queen of cheese.
May you not receive a scar as
We have heard that Mr. Harris
Intends to send you off as far as
The great world's show at Paris.
Of the youth beware of these,
For some of them might rudely squeeze
And bite your cheek, then songs or glees
We could not sing, oh! queen of cheese.
We'rt thou suspended from balloon,
You'd cast a shade even at noon,
Folks would think it was the moon
About to fall and crush them soon.
    '''

print(mammoth)

print('\n================================ RESTART ================================\n')

'''8. Импортируйте модуль re, чтобы использовать функции регулярных выражений в Python. 
Используйте функцию re.findall(), чтобы вывести на экран все слова, которые начинаются с буквы «с».'''

import re

pat = r'\bc\w*'
print(re.findall(pat, mammoth))

print('\n================================ RESTART ================================\n')

'''9. Найдите все четырехбуквенные слова, которые начинаются с буквы «c».'''

pat = r'\bc\w{3}\b'
print(re.findall(pat, mammoth))

print('\n================================ RESTART ================================\n')

'''10. Найдите все слова, которые заканчиваются на букву «r».'''

pat = r'\b[\w\']*r\b'
print(re.findall(pat, mammoth))

print('\n================================ RESTART ================================\n')

'''11. Найдите все слова, которые содержат три гласные подряд.'''

pat = r'\b\w*[AaEeIiOoUu]{3}\w*\b'
pat1 = r'\b\w*[aeiou]{3}[^aeiou\s]*\w*\b'
print(re.findall(pat, mammoth))
print(re.findall(pat1, mammoth))

print('\n================================ RESTART ================================\n')

'''12. Используйте метод unhexlify для того, чтобы преобразовать шестнадцатеричную строку, 
созданную путем объединения двух строк, что позволило ей разместиться на странице, 
в переменную типа bytes с именем gif:
'47494638396101000100800000000000ffffff21f9' +
'0401000000002c000000000100010000020144003b'
'''

import binascii

hex_str = '47494638396101000100800000000000ffffff21f9' + \
    '0401000000002c000000000100010000020144003b'
gif = binascii.unhexlify(hex_str)
print(len(gif))
print(gif)

print('\n================================ RESTART ================================\n')

'''13. Байты, содержащиеся в переменной gif, определяют однопиксельный прозрачный GIF-файл. 
Этот формат является одним из самых распространенных. Корректный файл формата GIF начинается со строки GIF89a. 
Является ли этот файл корректным?'''

print(type(gif))
print(type(b'GIF89a'))
print(gif[:6] == b'GIF89a')

print('\n================================ RESTART ================================\n')

'''14. Ширина файла формата GIF является шестнадцатибитным целым числом с обратным порядком байтов, 
которое начинается со смещения 6 байт. Его высота имеет такой же размер и начинается со смещения 8 байт. 
Извлеките и выведите на экран эти значения для переменной gif. Равны ли они 1?'''

import struct

width, height = struct.unpack('<HH', gif[6:10])
print(width, height)

