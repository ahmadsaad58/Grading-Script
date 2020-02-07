#!/bin/bash
echo ""
echo "+-------------------------------------+"
echo "|                                     |"
echo "|            Grader Creator           |"
echo "|                                     |"
echo "+-------------------------------------+"
echo ""

echo "This script creates folders for you to run test cases in. Every time you want to grade a new assignment, use this script."

echo ""

echo "Please enter the assignment number that you grading. This will create a folder called 'a<assignment number>'."
read assignment_num
folder_name=a$assignment_num

mkdir $folder_name

echo ""
echo "Creating Graded, Regrade, and Submissions folder in" $folder_name"..."

cd $folder_name
mkdir "Graded"
mkdir "Regrade"
mkdir "Submissions"

echo "Folders created..."
echo ""
echo "Copying Grade.py and Tools folder into" $folder_name"..."

cd ..

cp Grade.py ./$folder_name
cp -r Tools ./$folder_name

echo ""
echo "Copying prepare_grading.sh script into" $folder_name"..."
cp prepare_grading.sh ./$folder_name

echo ""
echo "Grading environment for assignment" $assignment_num "successfully created!"

echo ""
echo "Now, copy the submissions for assignment" $assignment_num "into" $folder_name"/Submissions. Create your own unit test python file, edit the CONST_TESTER to be that file in Grade.py, and then call Grade.py."
echo "Optionally, you can use prepare_grading.sh to move all the submissions (python files) from the Graded and Regrade folders back into the Submissions folder." 

