import winreg
import tkinter
from tkinter.simpledialog import askstring

REGISTRY_PATH = r"Software\AppsForVelti"

def get_credentials_from_registry():
	try:
		with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
			user = winreg.QueryValueEx(key, "user")[0]
			password = winreg.QueryValueEx(key, "password")[0]
			return user, password
	except FileNotFoundError:
		return None, None # No stored credentials

def store_credentials_to_registry(user, password):
	with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
		winreg.SetValueEx(key, "user", 0, winreg.REG_SZ, user)
		winreg.SetValueEx(key, "password", 0, winreg.REG_SZ, password)

def prompt_for_credentials():
	root = tkinter.Tk()
	root.withdraw() # Hide the root window
	user = askstring("", "Enter your Oracle username:")
	if not user:
		raise ValueError("Username is required.")
	password = askstring("", "Enter your Oracle password:")
	if not password:
		raise ValueError("Password is required.")
	return user, password

def initialize_credentials():
	# Attempt to get credentials from the registry
	user, password = get_credentials_from_registry()
	
	if not user or not password:
		print("Credentials not found. Prompting user...")
		user, password = prompt_for_credentials()
		store_credentials_to_registry(user, password)
		print("Credentials stored successfully.")
	
	return user, password