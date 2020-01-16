#  File: Bad_Sample.py

#  Description: A representation of a bad student file

#  Student Name: Bad Student

#  Student UT EID: ba123

#  Course Name: CS 313E

#  Unique Number: 85575

# Days Late: 2


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
	