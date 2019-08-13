# JiraPythonAPIUsage

## A simple script to use JIRA python API's to add and update JIRA tasks on the basis of an openvas html reports

A handy python script to ease out the pain of JIRA documentation.
The Script takes a directory identifies all the html reports and creates relative Jira tasks , assigns it to the creator, transitions it to "Done" on Kanban and changes resolution to "Done" after adding appropriate Description and Summary titles.


# Installation
``` pip install requirements.txt ```

# Usage

1)	Put all you html reports in a directory let’s say ```<directory>```
2)	Update happy.config with your Jira credentials and project name
3)	On the terminal run ```python jeher.py <directory>```





