from turtle import *
import random

def playing_area():
    pen = Turtle()
    pen.ht()
    pen.speed(0)
    pen.color('teal')
    pen.penup()
    pen.goto(-240,240)
    pen.pendown()
    pen.begin_fill()
    for _ in range(4):
        pen.forward(480)
        pen.right(90)
    pen.end_fill()

class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.speed(0)
        self.color(player.pcolor)
        self.shape("circle")
        self.shapesize(0.5, 0.5)
        self.penup()
        self.goto(player.xcor(),player.ycor())
        self.setheading(player.heading())
        self.forward(15)
        self.player = player
        self.showturtle()

    def move(self):
        self.forward(10)

class Player(Turtle):
    def __init__(self, x, y, color, screen, right_key, left_key, fire_key):
        super().__init__()
        self.ht()
        self.speed(0)
        self.pcolor = color
        self.color(color)
        self.penup()
        self.goto(x,y)
        self.setheading(90)
        self.shape("turtle")
        self.bullets = []
        self.alive = True
        self.health = 3
        self.st()
        
        screen.onkeypress(self.turn_left, left_key)
        screen.onkeypress(self.turn_right, right_key)
        screen.onkeypress(self.fire, fire_key)

    def fire(self):
        if self.alive:
            self.bullets.append(Bullet(self))

    def turn_left(self):
        if self.alive: self.left(10)
        
    def turn_right(self):
        if self.alive: self.right(10)

    def move(self):
        if not self.alive: return
        self.forward(2)
        if self.xcor() > 230 or self.xcor() < -230:
            self.setheading(180 - self.heading())
        if self.ycor() > 230 or self.ycor() < -230:
            self.setheading(-self.heading())

    def take_damage(self):
        self.health -= 1
        if self.health == 2:
            self.color("lightblue" if self.pcolor == "blue" else "#FFCCCC") # Lighter version
        elif self.health == 1:
            self.color("white")
        elif self.health <= 0:
            self.alive = False
            self.ht()
            self.clearbullets()

    def clearbullets(self):
        for b in self.bullets:
            b.ht()
            b.clear()
        self.bullets.clear()

screen = Screen()
screen.bgcolor("black")
screen.setup(600,600)
playing_area()

p1 = Player(-100, 0, "blue", screen, "d", "a", "w")
p2 = Player(100, 0, "red", screen, "Right", "Left", "Up")

def game_loop():
    for p in [p1, p2]:
        p.move()
        for bullet in p.bullets[:]:
            bullet.move()
            if abs(bullet.xcor()) > 250 or abs(bullet.ycor()) > 250:
                bullet.ht()
                p.bullets.remove(bullet)
                continue
            target = p2 if p == p1 else p1
            if bullet.distance(target) < 15 and target.alive:
                target.take_damage()
                bullet.ht()
                p.bullets.remove(bullet)

    screen.update()
    screen.ontimer(game_loop, 20)

screen.tracer(0)
game_loop()
screen.listen()
screen.mainloop()
