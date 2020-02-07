#  File: Half_Comp_Error.py

#  Description: A representation of a file with compiler errors

#  Student Name: Half Error

#  Student UT EID: he123

#  Course Name: CS 313E

#  Unique Number: 85575

# Days Late: 0

# say hello to user
def greet(name: str) -> str: 
	print "Hello, " + name + "!" )

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