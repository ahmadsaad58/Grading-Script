import sys
import subprocess
import os
import shutil
from typing import List, Tuple


# Important folders
CONST_REGRADE = "Regrade"
CONST_SUBMISSIONS = "Submissions"
CONST_GRADED = "Graded"

# testing script (may need to be changed depending on the test case file)
CONST_TESTER = "Test_Sample.py"

# file that student file will be copied to
CONST_COPY_DEST = "Test.py"
# temp file's name
CONST_TEMP_FILE = "temp.txt"

# append results to results.txt
ret = "results.txt"

# number of test cases (2 tests in this case)
CONST_NUM_TESTS = 2
CONST_COST_OF_TEST = 70 / CONST_NUM_TESTS 


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
    def grade(self) -> int: 
        self.fill_info()
        self.run_test_cases()
        self.calculate_grade()
        print('Failures', self.failures)
        print(self.file_to_grade)
        # print(self.error)
        # print(self.error_output)
        # TODO: may need to add more info
        return self.score

            

# Traverses files and grades them
def get_files(): 
    subdir = "./" + CONST_SUBMISSIONS
    process = subprocess.Popen(['ls', subdir], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    files = process.communicate()[0]
    files = files.decode()
    # creates and filters list
    files = files.split("\n")
    files = list(filter(lambda x: len(x) > 0 and x[-3:] == ".py", files))
    # traverse thru list
    for source in files:
        temp_student = Student(source)
        score = temp_student.grade()
        print(score)
    
    # remove files
    # os.remove(CONST_TEMP_FILE)
    # os.remove(CONST_COPY_DEST)


    
    
def main():
    get_files()
    

    


# def mainn():
    
#     process = subprocess.Popen(['ls', subdir], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
#     files = process.communicate()[0]
#     files = files.decode()

#     f = open(rfile, 'a')

#     for s in files.split('\n'):
#         if "" == s:
#             continue
#         s = s.strip()
#         eid, name, section, partner = extract_info(subdir + "/" + s)
#         if eid is "":
#             eid = "None"
#         if name is "":
#             name = "None"
#         if partner is "":
#             partner = "None"

#         src = open(subdir + "/" + s, 'r')
#         dst = open(copydir + "/" + s, 'w')
#         main_src = open("main.py", 'r')

#         for line in src:
#             if "main" in line:
#                 break
#             dst.write(line)

#         for line in main_src:
#             dst.write(line)

#         src.close()
#         dst.flush()
#         dst.close()
#         main_src.close()

#         score, comments = grade_assign(copydir + "/" + s)
#         scorestr = str("%.1f" % score)
#         f.write("%-8s %-20s    %5s   %s\n" % (eid, str(name)[-20:], scorestr, comments))
#         f.flush()
#     f.close()


 
 
if __name__ == "__main__":
    main()