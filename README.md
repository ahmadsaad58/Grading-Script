# Sample Grading Script

## Usage ##

	1. Clone this repo onto your machine.
	2. cd into this repo
	3. Run the command: "bash create_grading_folder.sh"
		A. The script contains instructions that will create a grading environment for you.
	4. Cd into the new folder that is created. It should be named "a<assignment_num>" if you followed the create_grading_folder.sh instructions correctly.
	5. Copy all of the submissions into the "Submissions" folder. 
		A. Make sure you are copying the submissions into the Submissions folder that is located inside of the grading environment.
		B. For example, if we were grading assignment1, you should copy submissions into "a1/Submissions"
	6. Copy your unit test file into your grading environment
	7. Change two variables int the "Grade.py" file. Change:
		A. CONST_TESTER = "Whatever your unit test file is called"
		B. CONST_NUM_TESTS = <However many tests there are>
	8. Make sure the Grade and Regrade folders are empty
	9. run "python3 Grade.py" to start the grading!
	10. If you want to rerun the grading script after you've already run it once:
		A. Run "bash prepare_grading.sh"
		B. Now you can run "python3 Grade.py" to grade again.

## Steps we need to take: ##

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
