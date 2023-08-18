from events import startEventListining
from config import *
from keep_alive import keep_alive

#start the  flask app
keep_alive()
#print(email)
#start the bot
startEventListining(email,password, session_cookies)
