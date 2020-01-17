# Sample Grading Script

Steps we need to take: 

	1. Get the all files from submissions and traverse them
	2. Move each file to the a temp Test.py file
	3. Run Sample_Test.py (the unittest file)
		A. pipe output to help and read from there
		B. Count the fails from help and return count
	4. Count points
	5. Count Comments
	6. Count the Header 
	7. Produce a score and move the original file based on score
		A. <= 30 then to regrade folder
		B. more than 30 then to CSV and graded folder
