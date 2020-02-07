# lacking header

# say hello to user
def greet(name: str) -> str: 
	return "Hello, " + name + "!"

# say good bye to user
def bye() -> str: 
	return "Good Bye!"

# main method
def main():
	my_name = "Good Student"
	print( greet(my_name) )
	print( bye() )


if __name__ == "__main__":
	main()
	