from tkinter import Y


class MyClass():
	def __init__(self, x , y):
		self.x = x
		self.y = y

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.x == other.x and self.y == other.y
		else:
			return False




a = MyClass(1,2)
b = MyClass(1,2)

x = set()
x.add(a)
x.add(b)

print(x)