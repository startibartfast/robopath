# Testing Tool for ABB Robotics Robotest Simulator
## Setup Instructions
0) Install Mysql Community Edition (https://dev.mysql.com/downloads/mysql/)
    - When asked select the simpler authentication method
    - Provide password for the default 'root' user as 'admin'. Both user name and password are hard-wired in the code (see module datamodel.py) ** IMPORTANT for safety reasons this should be used only on local machines not accessible by Internet **
    - When the installation is completed, create a database and call it 'robopath' (you can do it directly through the MySQL Command Line Client)
    
1) Download and install last stable python version (v.3.7.1). After the installation open a shell and run 'python -V' if everything is fine it should show python's version.

2) From a shell run: 'pip install virtualenv'

Creation of a virtual environment. virtualenv will create a folder named 'robopath' under <root_folder>
3) cd <root_folder>
4) run 'virtualenv robopath' 

5) Activate virtual environment run: '<root-folder>\robopath\Scripts\activate'. The shell prompt gets like: '(robopath) c:\<path>>'.
6) Install dependency packages. Run: pip install sqlalchemy, msql-connector-python, pymysql
7) Create a folder 'source' within <root-folder>\robopath
8) Copy all source files in <root-folder>\robopath\source
9) With a text editor open the file rpapp.py and:
    - Uncomment the line 'rpa.updateDatabase()' and save.
    - run 'python rpapp.py'
    - Comment the line 'rpa.updateDatabase()' and save.
10) Now the database structure is ready and you can run the app by the command 'python rpapp.py'
     