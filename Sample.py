# This file is serve as a representation of a student file that is turned in


# say hello to user
def greet(name: str) -> str: 
	return "Hello, " + name + "!"

# say good bye to user
def bye() -> str: 
	return "Good Bye!"

# main method
def main():
	my_name = "Saad"
	print( greet(my_name) )
	print( bye() )


if __name__ == "__main__":
	main()
	