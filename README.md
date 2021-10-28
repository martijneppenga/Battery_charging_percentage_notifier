# Battery_charging_percentage_notifier
Python program to notify user to start charging or stop charging laptop battery

The python program is designed to create a message box when the battery of the user needs charging, or when the user must stop charging. This can help to limit capacity performance losing of the battery over time. 

In general lithium ion batteries charge state should remain between 20-80 percent charge state for optimal battery life span.

The given code example will notify the user when the battery charge state if lower or equal to 25 percent, or when the charging state is higher or equal to 90 percent. 

A message box is used for the notification. The message box will disappear when the user closes the message box, or when a battery charging state change is encountered (i.e. from charging to discharging or vice versa). Furthermore, the battery percentage as well the charging state are printed to a console.

## Requirements
No third party package are required. Therefore no requirements.txt is added to this repository

Windows os only

## Start application at start up
Create a batch file or an executable and place the file in the following directory:
C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

### Create an executable
A executable can be created using pyinstaller https://pyinstaller.readthedocs.io/en/stable/
```bash
python pyinstaller --onefile Battery_percentage.py
```
### Create batch file
Open a text file and added the following line:<br>
python "path\to\directory\file\Battery_percentage.py"<br>
And change the extension from .txt to .bat
