from kivy.app import App #We need to import the bits of kivy we need as we need them as importing everything would slow the app down unnecessarily
from kivy.uix.widget import Widget #this is a thing that you want the App to display
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
#from kivy.uix.label import Label #this will import the code for the label in which we want to display Hello World!


class PongPaddle(Widget):

	score = NumericProperty(0)

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			print(ball.center_y, self.center_y,self.height)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
	# velocity of the ball on x and y axis
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	# referencelist property so we can use ball.velocity as
	# a shorthand, just like e.g. w.pos for w.x and w.y
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	# ``move`` function will move the ball one step. This
	#  will be called in equal intervals to animate the ball
	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def serve_ball(self, vel=(4, 0)):
		self.ball.center = self.center
		self.ball.velocity = vel

	def update(self, dt):
		self.ball.move()

		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

		if self.ball.y < self.y or self.ball.top > self.top:
			self.ball.velocity_y *= -1

		if self.ball.x < self.x:
			self.player2.score += 1
			self.serve_ball(vel=(4, 0))
		if self.ball.x > self.width:
			self.player1.score += 1
			self.serve_ball(vel=(-4, 0))

	def on_touch_move(self, touch):
		if touch.x < self.width / 3:
			self.player1.center_y = touch.y
		if touch.x > self.width - self.width / 3:
			self.player2.center_y = touch.y


class PongApp(App):
	#title = "Пинг Понг"
	def build(self):
		self.title = "Ping Pong"
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0/60.0)
		return game


if __name__ == '__main__': #Documentation suggests that each program file should be called main.py but I think that only matters if you're creating the final App to go onto a phone or tablet we're a long way off from that yet
	PongApp().run() #This must match the name of your App
