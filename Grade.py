import sys
import subprocess
import os
import shutil
import pandas as pd
from typing import List, Tuple


# Important folders
CONST_REGRADE = "Regrade"
CONST_SUBMISSIONS = "Submissions"
CONST_GRADED = "Graded"

# testing script (may need to be changed depending on the test case file)
CONST_TESTER = "Test_Sample.py"

# file that student file will be copied to, will be deleted by end
CONST_COPY_DEST = "Test.py"
# temp file's name
CONST_TEMP_FILE = "temp.txt"

# Graded CSV constant
CONST_CSV = "Graded.csv"

# append results to results.txt
CONST_ERR_FILE = "Fails.txt"

# number of test cases (2 tests in this case)
CONST_NUM_TESTS = 2
CONST_COST_OF_TEST = 70 / CONST_NUM_TESTS 
CONST_SCORE_CUTOFF = 30


# Student class that has all of the relevant assets for a single student
class Student(): 
    # creates dummy student
    def __init__(self, file_to_grade):
        # student file
        self.file_to_grade = CONST_SUBMISSIONS + "/" + file_to_grade
        self.num_lines = 0
        # student info
        self.student_name = None
        self.student_id = None
        self.partner = None
        self.partner_id = None
        # days late (-10 pts for each day)
        self.days_late = 0
        # student program assets
        self.failures = []
        self.comments = []
        self.score = 100
        # error flag
        self.error = [False, []]
        self.error_output = ""

    # fill student info from header and count comments (step 1)
    def fill_info(self):
        with open(self.file_to_grade, 'r') as student_file: 
            for line in student_file:
                self.num_lines += 1
                try: 
                    if "Student's Name" in line: 
                        self.student_name = line.strip().split(':')[1].strip()
                    elif "Student Name" in line:
                        self.student_name = line.strip().split(':')[1].strip()
                    elif "Student UT EID" in line:
                        self.student_id = line.strip().split(':')[1].strip()
                    elif "Student's UT EID" in line:
                        self.student_id = line.strip().split(':')[1].strip()
                    elif "Partner's Name" in line: 
                        name = line.strip().split(':')[1].strip()
                        self.partner = name if len(name) > 0 else None
                    elif "Partner Name" in line:
                        name = line.strip().split(':')[1].strip()
                        self.partner = name if len(name) > 0 else None
                    elif "Partner UT EID" in line:
                        eid = line.strip().split(':')[1].strip()
                        self.partner_id = eid if len(eid) > 0 else None
                    elif "Partner's UT EID" in line:
                        eid = line.strip().split(':')[1].strip()
                        self.partner_id = eid if len(eid) > 0 else None
                    elif "Days Late" in line:
                        late = line.strip().split(':')[1].strip()
                        self.days_late = int(late) if late else 0
                    elif "Day Late" in line:
                        late = line.strip().split(':')[1].strip()
                        self.days_late = int(late) if late else 0
                    # counts comments
                    if "#" in line: 
                        # will count header, leave it for a little better grade
                        self.comments.append(line.strip())
                except:
                    self.error = [True, ["Header Info incorrect"]]
    
        if not self.student_name or not self.student_id: 
            self.error = [True, ["Header Info incorrect"]]

        
    
    # actual grading (step 2)
    def run_test_cases(self):
        # takes the file and copies to temp test file
        shutil.copyfile(self.file_to_grade, CONST_COPY_DEST) 

        # calls Test_Sample.py now and pipes to help.txt
        os.system('python3 ' + CONST_TESTER + ' 2> ' + CONST_TEMP_FILE)
    
        # store errors that can be later piped to a file
        temp_error_store = []

        # open piped file and 
        with open(CONST_TEMP_FILE) as piped_file: 
            for line in piped_file: 
                # add each line in case of error
                temp_error_store.append(line)
                
                curr = line.strip()
                # catch the failures
                if curr[:4] == "FAIL":
                    self.failures.append(curr)

                # catch the assertion error from Unittest framework
                if "AssertionError:" in curr: 
                    continue
                
                # Catch the compile time error
                if "Error" in curr: 
                    self.error[0] = True
                    self.error[1].append( "Error in compiling, rerun: " + curr ) 
                    self.error_output = "".join(temp_error_store)


    
        # pop last failure as it is extra
        if len(self.failures) > 0:
            self.failures.pop()

    # calculating the score (Step 3)
    # 70 pts from test cases + 30 pts from comments/style
    def calculate_grade(self):
        
        # Check the errors
        if self.error[1]: 
            for error in self.error[1]:
                # points off for bad header
                if error == "Header Info incorrect":
                    self.score -= 5
                # 0 points for any error
                if "Error in compiling," in error:
                    self.score = 0
                    return
        
        # points for late and each test case
        self.score -= 10 * self.days_late
        self.score -= len(self.failures) * CONST_COST_OF_TEST
        
        # score the comments
        if len(self.comments) < (self.num_lines / 30):
            self.score -= 30
        elif len(self.comments) < (self.num_lines / 20):
            self.score -= 20
        

    
    # runs all the steps in sequence 
    def grade(self): 
        # calls the functions
        self.fill_info()
        self.run_test_cases()
        self.calculate_grade()

        # checks whether error and above cutoff
        return (not self.error[0]) and (self.score >= CONST_SCORE_CUTOFF)

            

# Traverses files and grades them
def get_files(): 

    # See if csv is there
    subdir = "./" + CONST_GRADED
    process = subprocess.Popen(['ls', subdir], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    files = process.communicate()[0]
    files = files.decode()
    files = files.split("\n")
    
    # if it is read it in, else make new frame
    if CONST_CSV in files: 
        frame = pd.read_csv(subdir + "/" + CONST_CSV)
    else:
        # creating the csv frame for graded assignments
        frame = pd.DataFrame(columns=["Name", "EID", "Score", "Failures"])

    # traverse files in graded
    subdir = "./" + CONST_SUBMISSIONS
    process = subprocess.Popen(['ls', subdir], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    files = process.communicate()[0]
    files = files.decode()
    # creates and filters list
    files = files.split("\n")
    files = list(filter(lambda x: len(x) > 0 and x[-3:] == ".py", files))
    
    # list of series/rows for csv
    series = []

    # traverse thru list
    for source in files:
        # create and grade student
        temp_student = Student(source)
        write_to_csv = temp_student.grade()
        # what file we are moving
        file_to_move = "./" + CONST_SUBMISSIONS + "/" + source
        
        # add to dataframe
        if write_to_csv:
            row = [ temp_student.student_name, temp_student.student_id, temp_student.score, " | ".join(temp_student.failures) ]
            series.append(pd.Series(row, index=frame.columns))
            
            # TODO: move to graded.
            # shutil.move(file_to_move, + "./" + CONST_GRADED) 
        
        else: 
            # open the error file
            with open(CONST_REGRADE + "/" + CONST_ERR_FILE, mode="a+") as error_file:
                # find name, whether it exists or not
                if not temp_student.student_name:
                    name = temp_student.file_to_grade.split('/')[-1]
                    name = name[:-3]
                else: 
                    name = temp_student.student_name
                    
                # gather errors and write them
                errors = temp_student.error_output if len(temp_student.error_output) > 0 else "NO ERRORS"
                error_file.write("\n" + name + "    |    " + str(temp_student.score) + "\n" + errors + "\n")
                
                # TODO: move to regrade
                # shutil.move(file_to_move, + "./" + CONST_REGRADE) 

            
    
    # add frame to csv
    frame = frame.append(series, ignore_index=True)
    subdir = "./" + CONST_GRADED
    frame.to_csv(subdir + "/" + CONST_CSV)
    # remove files
    os.remove(CONST_TEMP_FILE)
    os.remove(CONST_COPY_DEST)

   
def main():
    get_files()
    print("WOOOOOO YOU ARE DONE")
    

if __name__ == "__main__":
    main()