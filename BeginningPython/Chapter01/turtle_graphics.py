from turtle import *
import math

igor = Turtle(shape='turtle')

igor.speed(1)

igor.forward(100)
igor.left(120)
igor.forward(100)
igor.left(120)
igor.forward(100)

sonya = Turtle(shape='turtle')

sonya.color("blue", "cyan")
# octagon
sonya.begin_fill()
sonya.forward(100)
sonya.setheading(45)
sonya.forward(100)
sonya.setheading(90)
sonya.forward(100)
sonya.setheading(135)
sonya.forward(100)
sonya.setheading(180)
sonya.forward(100)
sonya.setheading(225)
sonya.forward(100)
sonya.setheading(270)
sonya.forward(100)
sonya.setheading(315)
sonya.forward(100)

tanya = Turtle(shape='turtle')
tanya.color("red")

tanya.penup()
tanya.setheading(45)
tanya.left(45)
tanya.forward(100)
tanya.pendown()

tanya.begin_fill()
for i in range(8):
    tanya.forward(200)
    tanya.left(135)
tanya.end_fill()

irina = Turtle(shape='turtle')
irina.left(500)
irina.color("red", "yellow")
irina.speed(10)

irina.begin_fill()
for i in range(100):
    irina.forward(math.sqrt(i)*10)
    irina.left(168.5)
irina.end_fill()

zina = Turtle(shape='turtle')
zina.color("green")
zina.speed(30)
zina.penup()
zina.left(500)
zina.forward(100)
zina.pendown()

for i in range(100):
    zina.forward(10)
    zina.forward(math.sin(i/10)*25)
    zina.left(20)

nord = Turtle(shape='turtle')
nord.color("white")
nord.getscreen().bgcolor("#994444")

def star(nord):
    nord.forward(200)
    nord.left(216)
    nord.forward(200)
    nord.left(216)
    nord.forward(200)
    nord.left(216)
    nord.forward(200)
    nord.left(216)
    nord.forward(200)
    nord.left(216)
    nord.forward(200)
    nord.left(216)

star(nord)

done()
