import re
import info
import winsound
import oracledb
import credentials
from pathlib import Path

home = str(Path.home())
oracledb.init_oracle_client(home + "\\instantclient")
db_user, db_password = credentials.initialize_credentials()

def check_status_in_db(msisdn):
# Function to check MSISDN status
	try:
		# Use "with" to ensure the connection is closed after the block
		with oracledb.connect(
			user = db_user,
			password = db_password,
			host = info.host,
			service_name = info.service
		) as connection:
			# Use "with" to ensure the cursor is closed after the block
			with connection.cursor() as cursor:
				# Query to check if the MSISDN has status = "ACTIVE"
				query = info.query1
				cursor.execute(query, input = msisdn)
				result = cursor.fetchone()
				
				# Check if the MSISDN has a row and return True if status is ACTIVE
				return (result and result[0] == 'ACTIVE')
	
	except oracledb.Error as e:
		error_message = str(e)
		print(f"Database error occurred: {error_message}")
		
		# Check for invalid login error (ORA-01017)
		if re.search(r'ORA-01017', error_message):
			print("Invalid login credentials. Prompting user...\n")
			user, password = credentials.prompt_for_credentials()
			credentials.store_credentials_to_registry(user, password)
		else:
			print("An unexpected database error occurred.\n")
			
		exit(1)
		return False

def check_results_in_db():
	try:
		# Using "with" to ensure the connection is closed after the block
		with oracledb.connect(
			user = db_user,
			password = db_password,
			host = info.host,
			service_name = info.service
		) as connection:
			# Using "with" to ensure the cursor is closed after the block
			with connection.cursor() as cursor:
				# Query to check if the procedure is done
				cursor.execute(info.query2)
				result = cursor.fetchone()
				
				if (result and result[0] == 'SUCCESS'):
					print("Procedure executed successfully.\n")
					
					# Query to get the results of the procedure
					cursor.execute(info.query3)
					
					result = cursor.fetchall()
					
					if result:
						print("DB accessed, data returned.\nLines : " + str(len(result)) + "\n")
						return result
				else:
					print("Procedure not executed, rerunning in 1min.\n")
					return None
	
	except oracledb.Error as e:
		winsound.MessageBeep(winsound.MB_ICONASTERISK)
		print(f"{info.error}: {e}")
		exit(1) # Close the application.
		return False
