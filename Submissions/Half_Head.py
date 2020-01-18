#  File: Half_Head.py

#  Student Name: Headless Error

# Days Late: 0

# say hello to user
def greet(name: str) -> str: 
	return "Hello, " + name + "!"

# say good bye to user
def bye() -> str: 
	return "Good Bye!"

# main method
def main():
	my_name = "Compile Error"
	print( greet(my_name) )
	print( bye() )


if __name__ == "__main__":
	main()