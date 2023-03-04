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

def func(*args, **kwargs):
	print(f"args = {args}")
	print(f"kwargs = {kwargs}")


def func2(a, *, arg1=None, arg2=None, arg3=None):
	
	print(f"arg1 = {arg1}")
	print(f"arg2 = {arg2}")
	print(f"arg3 = {arg3}")


func2(1,arg1="jeff")
func(*["one", "two", "three"], epic="fart")