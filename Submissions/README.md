## Submissions Folder

This folder contains all of the submissions for a particular assignment. This should be run in batch as the overhead of starting and setting up the script on a single TA's machine may hinder in efficiency. The files once graded and tallied on the CSV files will be moved to the correct folder. 

A file needs to be regraded, if it has an error/no header or if the score is too low (the score cutoff is a constant you can set in Grade.py). The files that need to be regraded will be moved to the regrade folder with a file of their errors. <i> Future scripts can be created to divide the regrade files into folders for TAs to grade </i>

The grades and comments will be available in a <i>CSV file </i> and should be uploaded to Google Drive for the other TAs to reference

#### These files be graded only once and are moved for that reason

### The Files in this Folder
<i> The files in this folder are for testing how robust the grading script is, if you would like to add more tests, feel free to fork </i>

- Bad_Sample.py: Wrong output
	- Move to graded folder and low points
- Comp_Error_No_Head.py: Compiler Error and No header
	- Moved to regrade, name is file name
- Compile_Error.py: Compiler Error
	- Moved to regrade
- Empty.py: Empty file
	- Moved to regrade
- Half_Comp_Error.py: 1 function has a compiler error 
	- Moved to regrade as there could more errors 
- Half_Head.py: Half of the header is present
	- Move to regrade to better assess the issue
- No_Comment.py: No comments/header
	- Move to regrade since no header
- No_Header.py: No header
	- Move to regrade to better assess the issue
- Sample.py: Perfect
	- Move to grade 

<i> This should take care of all the tests as it covers all the different cases present </i>