import time
import info
import pyperclip

def copy_email():
	# Copy the email template on clipboard
	pyperclip.copy(info.email)

def copy_queries():
	# Copy the queries to clipboard
	pyperclip.copy(info.query2)
	time.sleep(1)
