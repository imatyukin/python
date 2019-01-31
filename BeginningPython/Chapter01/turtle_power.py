from random import randint
from turtle import Turtle, Screen

class MyTurtle(Turtle):

    def petals(self, size=30, count=8, speed=100):
        if size == 30:
            self.begin_fill()

        if size > 0:  # drawing leading edge of petal
            self.fd(3)
            self.rt(3)

            screen.ontimer(lambda: self.petals(size - 1, count, speed), speed)
            return

        if size == 0:  # switch to other edge of petal
            self.rt(90)

        if size > -30:  # drawing trailing edge of petal
            self.fd(3)
            self.rt(3)

            screen.ontimer(lambda: self.petals(size - 1, count, speed), speed)
            return

        self.end_fill()  # finish this petal
        self.lt(230) # prepare for the next petal

        if count > 0:  # drawing the next petal
            screen.ontimer(lambda: self.petals(count=count - 1, speed=speed), speed)
            return

        self.hideturtle()  # finished drawing

    def flowerhead(self):
        self.pencolor('red')   # outlines the flowerpetals in red to see easier
        self.petals(speed=9)

       # self.petals(speed=randint(50, 250))

def flower1():
    todd.color('green', 'blue')
    todd.goto(0, -270)
    todd.penup()
    todd.showturtle()
    todd.goto(0,0)
    todd.pendown()
    todd.flowerhead()

def flower2():
    tony.color('green', 'purple')
    tony.penup()
    tony.goto(0, -200)
    tony.pendown()
    tony.showturtle()
    tony.goto(80, -15)
    tony.seth(0)
    tony.flowerhead()

def flower3():
    tina.color('green', 'turquoise')
    tina.penup()
    tina.goto(0, -200)
    tina.pendown()
    tina.showturtle()
    tina.goto(-80, -15)
    tina.seth(90)
    tina.flowerhead()

def flower4():
    tiny.color('green', 'black')
    tiny.penup()
    tiny.goto(0, -200)
    tiny.pendown()
    tiny.showturtle()
    tiny.goto(160, -25)
    tiny.seth(90)
    tiny.flowerhead()


def flower5():
    tweeny.color('green', 'pink')
    tweeny.penup()
    tweeny.goto(0, -200)
    tweeny.pendown()
    tweeny.showturtle()
    tweeny.goto(-160, -25)
    tweeny.seth(90)
    tweeny.flowerhead()

def writing():
    teacher.penup()
    teacher.setpos(0, 120)
    teacher.pendown()
    teacher.color('red')
    teacher.write('To you!', align='center', font=('Times New Roman', 30, 'normal'))

tony = MyTurtle(shape='turtle', visible=False)
todd = MyTurtle(shape='turtle', visible=False)
tina = MyTurtle(shape='turtle', visible=False)
tiny = MyTurtle(shape='turtle', visible=False)
tweeny = MyTurtle(shape='turtle', visible=False)
teacher = MyTurtle(shape='turtle', visible=False)

screen = Screen()
screen.title('I am epic')
screen.delay(0)

screen.ontimer(flower2, 6500)
screen.ontimer(flower4, 0)
screen.ontimer(flower3, 6500)
screen.ontimer(flower5, 0)
screen.ontimer(flower1, 13000)

screen.ontimer(writing, 26000)

screen.mainloop()