# DigiBill
## Installation
1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

Now you should be ready to run the project!

## Usage 
1. It is essential first to run the `database.py` file. This will create a folder with the name instance and a file `receipts.db`. If this file is created outside of the `receipt_manager` folder, you should move it inside such that it looks like the directory below. 
![image](https://github.com/bramlouwerens1/DigiBill/assets/169822285/5a09019e-d7bf-40c1-a673-9a61f0bfc54e)

2. Next, run the `app.py`. When doing so, the flask program will start to host a server. In the terminal, a link will appear that brings you to the application.
3. Now you're ready to manage your bills!

## Description
The receipt folder in the templates allow the html interface to work on the server interactively with the functions that have been defined in the app.py file
