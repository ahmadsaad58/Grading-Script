# This file is serve as a representation of a bad student file 

# say hello to user
def greet(name: str) -> str: 
	return "heLO, " + name + "?"

# say good bye to user
def bye() -> str: 
	return "G00D daY!"

# main method
def main():
	my_name = "Bad Student"
	print( greet(my_name) )
	print( bye() )


if __name__ == "__main__":
	main()
	