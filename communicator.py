#Communication
import pandas as pd
import smtplib
import imaplib
import os
import subprocess
from mailcow import MailCow

result = subprocess.run(
    [],
    text = True,
    check = True
    timeout = 10
)

os.name == platform.system()
print(os.name)

if os.name == 'Windows':
    print("USERS DEVICE IS RUNNING: Windows")
elif os.name == 'Linux':
    print("USER'S DEVICE IS RUNNING: Linux")
elif os.name == 'Darwin':
    print("")