
def greet(name: str) -> str: 
	return "Hello, " + name + "!"


def bye() -> str: 
	return "Good Bye!"


def main():
	my_name = "Good Student"
	print( greet(my_name) )
	print( bye() )


if __name__ == "__main__":
	main()