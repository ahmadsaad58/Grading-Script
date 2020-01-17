import sys
import subprocess
import signal
import re
import os
import shutil
import errno
from typing import List


# Important file structure 
errdir = "Regrade"
copydir = "Submissions"
enddir = "Graded"

# file that student file will be copied to
copydest = "Test.py"

# testing script (may need to be changed depending on the test case)
tester = "Test_Sample.py"

# append results to results.txt
ret = "results.txt"



# gets the files and returns a list to be traversed
def get_files() -> List[str]: 
    subdir = "./" + copydir
    process = subprocess.Popen(['ls', subdir], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    files = process.communicate()[0]
    files = files.decode()
    
    # returns list of files
    return files.split("\n")


# traverses the files and appends to results
def traverse_files(files: list):
    # loops thru the files
    for source in files:
        if source[-3:] == ".py": 
            src = copydir + "/" + source
            # fills the test file
            shutil.copyfile(src, copydest) 
            grade(tester)


def grade(tester: str) -> int, List[str]:
    # working in Test_Sample.py now
    os.system('python3 Test_Sample.py 2> help.txt')
    
    with open("help.txt") as f: 
       for line in f: 
           print(line.strip())
    
    

    



def run():
    traverse_files(get_files())

run()


def main():
    global subdir
    global copydir
    global errdir

    start_submission = None
    end_submission = None


    process = subprocess.Popen(['ls', subdir], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    files = process.communicate()[0]
    files = files.decode()

    f = open(rfile, 'a')

    for s in files.split('\n'):
        if "" == s:
            continue
        s = s.strip()
        eid, name, section, partner = extract_info(subdir + "/" + s)
        if eid is "":
            eid = "None"
        if name is "":
            name = "None"
        if partner is "":
            partner = "None"

        src = open(subdir + "/" + s, 'r')
        dst = open(copydir + "/" + s, 'w')
        main_src = open("main.py", 'r')

        for line in src:
            if "main" in line:
                break
            dst.write(line)

        for line in main_src:
            dst.write(line)

        src.close()
        dst.flush()
        dst.close()
        main_src.close()

        score, comments = grade_assign(copydir + "/" + s)
        scorestr = str("%.1f" % score)
        f.write("%-8s %-20s    %5s   %s\n" % (eid, str(name)[-20:], scorestr, comments))
        f.flush()
    f.close()

def extract_info(filetograde):
    fh = open(filetograde, 'r')
    eid = None
    name = None
    section = None
    partner = None

    for line in fh:
        try:
            if "Student UT EID" in line:
                eid = line.strip().split(':')[1].strip()
            elif "Student's UT EID" in line:
                eid = line.strip().split(':')[1].strip()
            elif "Student's Name" in line:
                name = line.strip().split(':')[1].strip()
            elif "Student Name" in line:
                name = line.strip().split(':')[1].strip()
            elif "Unique Number" in line:
                section = line.strip().split(':')[1].strip()
            elif "Partner's Name" in line:
                partner = line.strip().split(':')[1].strip()
            elif "Partner Name" in line:
                partner = line.strip().split(':')[1].strip()
        except:
            print ("Student did not fill their information correctly")
            continue

    fh.close()
    print (eid,name,section,partner)
    print("The execution time can take too long. In this case, you can press ctrl+C. Grading script will move this submission to errdir. So, you can grade it later")
    return (eid, name, section, partner)

# actual grading
def grade_assign(filetograde):
    grade_comments = ''
    results = []
    score = 0
    comment_score = 0

    try:
        process = subprocess.Popen(['python3', filetograde], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        result = process.communicate()[0]
        result = result.decode()

        result = result.split('\n')
        try:
            while True:
                result.remove('')
        except:
            pass

        for line in result:
            if ":" not in line:
                continue
            if "True" in line:
                results.append(["True", line.strip()])
            elif "False" in line:
                results.append(["False", line.strip()])
            elif "fail" in line:
                results.append(["error", line.strip()])
            else:
                to_add = re.findall("/d+", line.strip())
                if len(to_add) > 0:
                    results.append([to_add, line.strip()])
                else:
                    results.append(["error", line.strip()])

        try:
            while True:
                results.remove([])
        except:
            pass

        for i in range(len(answers)):
            if answers[i][0] == results[i][0]:
                print("Student (pass): ", results[i][0])
                score += 2
            else:
                print("Student (fail): ", results[i][0])
                grade_comments += results[i][1].split()[0] + " tested incorrect. "
                print("       Correct: ", answers[i][0])
            print()

        print()
        print("Current score out of 100: " + str(score))
        try:
            score = int(input("Is that correct? If so, hit enter. If not, enter new score: "))
        except ValueError:
            pass

        fh = open(filetograde, 'r')
        commented = False
        comments = []
        for line in fh:
            if "main" in line:
                break
            print (line, end='')
            if '#' in line.strip():
                if ('File' in line.strip()) or ('Description' in line.strip()) or ('Student' in line.strip()) or ('Course' in line.strip()) or ('Unique' in line.strip()) or ('Date' in line.strip()) or ('Partner' in line.strip()):
                    continue
                else:
                    commented = True
                    comments.append(line.strip())
        fh.close()



        try:
            score += int(input('Score for program design? (default 20 out of 20): '))
        except ValueError:
            score += 20

        try:
            score += int(input("Score for coding style (default 20 out of 20): "))
        except ValueError:
            score += 20

        if commented:
            try:
                print("    Comments:")
                for comment in comments:
                    print('\t'+comment)
                comment_score = int(input("Detected at least one new comment printed above (please verify). Score for comments (default 10 out of 10): "))
            except ValueError:
                comment_score = 10
        else:
            try:
                grade_comments += "Need to comment code. "
                comment_score = int(input("Detected no new comments (please verify). Score for comments (default 0 out of 10): "))
            except ValueError:
                comment_score = 0

        if ('late' in filetograde):
            try:
                late_date = int(input("This is late submission, please enter days late. (default: 1): "))
                score -= (10 * late_date)
            except ValueError:
                score -= 10
            except SyntaxError:
                score -= 10

        print("Final Score: ", score+comment_score)
        print("Current Comments: ", grade_comments)
        try:
            grade_comments += input("Additional Comments: ")
        except ValueError:
            pass

    except KeyboardInterrupt:
        subprocess.Popen(['cp', './' + str(filetograde), './' + str(errdir) + '/'])
        score = 0
        print()
    except Exception as ex:
        try:
            input("Error: " + str(ex) + " This student's submission made errors while working on grading scripts. This file will be moved to error directory and score of this student will be stored as 0. Please manually check it. Please hit enter.")
        except:
            pass
        subprocess.Popen(['cp', './' + str(filetograde), './' + str(errdir) + '/'])
        score = 0

    return score+comment_score, grade_comments

# main()