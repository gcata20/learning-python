# **Description**
I started my journey with Python in January of 2024 by taking [CS50's Introduction to Programming with Python](https://www.harvardonline.harvard.edu/course/cs50s-introduction-programming-python). Having had some prior experience with C and C#, I took to it rather quickly. Ten weeks of informative lectures and somewhat challenging problem sets culminated in a final project for which I wrote a simple Password Manager. In this app, users could set up accounts and interact with a database to create and manage their entries through a humble text-based UI. 

With the course completed, I wanted to delve deeper into Python by coding a few small apps. I created this repository to learn more about Git as well and bundle these projects together into one convenient location.

&nbsp;

# **Projects**

### **Contact Manager**

Keeps track of all your contact details. Each contact must have a unique name, everything else can be left blank or filled in with your desired input. Emails and birthdays are checked for validity using regular expressions. Birthdays are also checked to see if the dates exist using the datetime module.
- **email pattern**: *name@domain*
  - **name**: one or more letters (lower and uppercase), digits, underscores, dashes and dots
  - **domain**: one or more characters of any kind except for @
- **birthday pattern**: *YYYY-MM-DD*
  - use leading zeroes for single-digit days or months (example: 1985-01-09) 

### **File Sorter**
Moves all files from a source folder into categorized subfolders. Input the folder you want sorted and the program will take care of the rest. It loops through each file, matches its extension to a category using a dictionary, creates a subfolder for that category (if one doesn't exist already) and moves the file there. Any files with unrecognized extensions will be moved into a separate subfolder.

### **Hangman**
The popular game, reimagined as a Python exercise. Play however many games you want and try to win by guessing all letters or the entire word at once. The code reads the "words.txt" file into a list in order to choose a random word at the start of every game so feel free to modify it by adding your own words.

### **Password Generator**
Generates random passwords. Input your desired length and watch the magic happen. The passwords contain both lowercase and uppercase letters as well as digits. It can easily be modified to include any other special characters you may want for extra security.
